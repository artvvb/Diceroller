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


if __name__ == "__main__":
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
		