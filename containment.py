def dot_product(a,b):
	return a.x*b.x+a.y*b.y

class TriangleContainment:
	def __init__(self):
		return
	def triangle_contains(self, a, b, c, p):
		raise NotImplementedError()
	def triangle_contains_any(self, a, b, c, L_p):
		raise NotImplementedError()
	def triangle_contains_all(self, a, b, c, L_p):
		raise NotImplementedError()
	def any_triangles_contain(self, L_a, L_b, L_c, p):
		raise NotImplementedError()
	def all_triangles_contain(self, L_a, L_b, L_c, p):
		raise NotImplementedError()
	
class BarycenterMethod(TriangleContainment):
	def __init__(self):
		return
	def _set_triangle(self, t):
		self.a,self.b,self.c = t[0],t[1],t[2]
		self.v0 = self.c - self.a
		self.v1 = self.b - self.a
		self.dot00 = dot_product( self.v0, self.v0 )
		self.dot01 = dot_product( self.v0, self.v1 )
		self.dot11 = dot_product( self.v1, self.v1 )
		self.invDenom = 1.0 / (self.dot00 * self.dot11 - self.dot01 * self.dot01)
	def _triangle_containment(self):
		self.v2 = self.p - self.a
		self.dot02 = dot_product( self.v0, self.v2 )
		self.dot12 = dot_product( self.v1, self.v2 )
		self.u = (self.dot11 * self.dot02 - self.dot01 * self.dot12) * self.invDenom
		self.v = (self.dot00 * self.dot12 - self.dot01 * self.dot02) * self.invDenom
		return (self.u >= 0) and (self.v >= 0) and (self.u + self.v < 1)
	def _set_point(self, p):
		self.p = p
	def triangle_contains(self, t, p):
		self._set_point( p )
		self._set_triangle( t )
		return self._triangle_containment()
	def triangle_contains_any(self, t, L_p):
		self._set_triangle( t )
		for p in L_p:
			self._set_point( p )
			if self._triangle_containment():
				return True
		return False
	def triangle_contains_all(self, t, L_p):
		self._set_triangle( t )
		for p in L_p:
			self._set_point(p)
			if not self._triangle_containment():
				return False
		return True
	def any_triangles_contain(self, L_t, p):
		self._set_point( p )
		for t in L_t:
			self._set_triangle( t )
			if self._triangle_containment():
				return True
		return False
	def all_triangles_contain(self, L_t, p):
		self._set_point( p )
		for t in L_t:
			self._set_triangle( t )
			if not self._triangle_containment():
				return False
		return True

class AreaMethod(TriangleContainment):
	def __init__(self):
		return
	def _compute_area(self, t):
		temp = (t[0].x-t[2].x)*(t[1].y-t[0].x)-(t[0].x-t[1].x)*(t[2].y-t[0].y)
		if temp < 0: temp *= -1
		return temp/2
	def triangle_contains(self, t, p):
		a0 = self._compute_area( t )
		a1 = self._compute_area( t )
		a2 = self._compute_area( t )
		a3 = self._compute_area( t )
		return a0 == a1+a2+a3

		
class LineSegmentIntersection:
	#Usage: use this class to stream a set of line segments to compare against a single one, or just compare two segments
	def __init__(self):
		return
	def _set_L1(self, L1, setdenom = False):
		self.x1 = L1[0].x
		self.y1 = L1[0].y
		self.x2 = L1[1].x
		self.y2 = L1[1].y
		self.numer_1 = (self.x1*self.y2-self.y1*self.x2)
	def _set_L2(self, L2):
		self.x3 = L2[0].x
		self.y3 = L2[0].y
		self.x4 = L2[1].x
		self.y4 = L2[1].y
		self.numer_2 = (self.x3*self.y4-self.y3*self.x4)
	def _compute_intersection(self, fail_if_oob=False):
		self.denom = ((self.x1-self.x2)*(self.y3-self.y4) - (self.y1-self.y2)*(self.x3-self.x4))
		if self.denom == 0:
			return None
		else:
			result = (
				(self.numer_1*(self.x3-self.x4) - (self.x1-self.x2)*self.numer_2) / self.denom,
				(self.numer_1*(self.y3-self.y4) - (self.y1-self.y2)*self.numer_2) / self.denom
			)
			if fail_if_oob: # return None if intersection is outside of either line segment's bounds
				raise NotImplementedError()
			else:
				return result
	def get_intersection(self, L1, L2):
		self._set_L1(L1)
		self._set_L2(L2)
		return self._compute_intersection()
	def get_intersections(self, L1, LL2):
		self._set_L1(L1)
		LI = []
		for L2 in LL2:
			self._set_L2(L2)
			LI.append(self._compute_intersection())
		return LI
		

if __name__ == "__main__":
	"""
	print("Benchmarking Available TriangleContainment Components:")
	import datetime
	L_t = []
	L_r = []
	a,b,c = (-340,495),(-153,-910),(835,-947)
	x,y,z = (-175, 41),(-421,-714),(574,-645)
	p = (0,0)
	bary_comp = BarycenterMethod()
	area_comp = AreaMethod()
	L_t.append( datetime.datetime.now() )
	L_r.append( bary_comp.triangle_contains( a , b , c , p ) )
	L_r.append( bary_comp.triangle_contains( x , y , z , p ) )
	L_t.append( datetime.datetime.now() )
	L_r.append( area_comp.triangle_contains( a , b , c , p ) )
	L_r.append( area_comp.triangle_contains( x , y , z , p ) )
	L_t.append( datetime.datetime.now() )
	print((L_t[1]-L_t[0]).microseconds, (L_t[2]-L_t[1]).microseconds)
	print(L_r)
	
	
	#TODO: create a benchmark based on import random or project euler problem #102
	#"""
	import coord
	mysquare = [
		(coord.Coord(x=0,y=0),coord.Coord(x=0,y=1)),
		(coord.Coord(x=0,y=1),coord.Coord(x=1,y=1)),
		(coord.Coord(x=1,y=1),coord.Coord(x=1,y=0)),
		(coord.Coord(x=1,y=0),coord.Coord(x=0,y=0))
	]
	mysegment = (coord.Coord(x=-1,y=-1),coord.Coord(x=2,y=-1))
	LS = LineSegmentIntersection()
	results = LS.get_intersections(mysegment, mysquare)
	for c in results:
		print(c)