from OpenGL.GL import *
import coord
import containment
import math

def rotate(c, center, rad):
	vec = c - center
	cs = math.cos(rad)
	sn = math.sin(rad)
	return coord.Coord (
		x = vec.x * cs - vec.y * sn,
		y = vec.x * sn + vec.y * cs
	) + center

def dummy_update(obj):
	pass
	
CONTAINMENT_OBJ = containment.BarycenterMethod()
	
class RegularPolygon:
	def __init__(self, vertex_count, center, radius, rotation_rad, layer):
		self.layer, self.center, self.vertex_count = layer, center, vertex_count
		update = dummy_update
		base_vertex = self.center + coord.Coord(x=radius, y=0.0)
		base_vertex = rotate(base_vertex, self.center, rotation_rad)
		rad_between_vertices = 2*math.pi / vertex_count
		self.vertices = [rotate(base_vertex, self.center, x * rad_between_vertices) for x in range(vertex_count)]
		
	def contains(self, c):
		return CONTAINMENT_OBJ.any_triangles_contain(self.triangles, c)
		
	def set_update(self, update):
		self.update = update
		
	def rotate(self, rad):
		self.vertices = [rotate(vertex, self.center, rad) for vertex in self.vertices]
		
	def move(self, vec):
		self.center += vec
		self.vertices = [vertex + vec for vertex in self.vertices]
		
class ClickableObject():
	def __init__(self):
		self.selected = False
		self.hover = False
	def select(self, new_center):
		self.center = new_center
		self.selected = True
	def deselect(self):
		self.selected = False
		
class DrawMethod:
	def draw(self):
		glBegin(self.gl_property)
		for vertex in self.vertices: glVertex2f(vertex.x, vertex.y)
		glEnd()
		
class TriangleStrip(DrawMethod):
	def __init__(self, vertices):
		self.vertices = vertices
		self.gl_property = GL_TRIANGLE_STRIP
	@property
	def triangles(self):
		i = 0
		while i+2 < len(self.vertices):
			yield self.vertices[i:i+3]
			i += 1
			
class TriangleFan(DrawMethod):
	def __init__(self, vertices):
		self.vertices = vertices
		self.gl_property = GL_TRIANGLE_FAN
		
	@property
	def triangles(self):
		i = 1
		while i+1 < len(self.vertices):
			yield [self.vertices[0], self.vertices[i], self.vertices[i+1]]
			i += 1
		
class RegularHexagon(RegularPolygon):
	@property
	def triangle_strip(self):
		return TriangleStrip([
			self.vertices[1],
			self.vertices[2],
			self.vertices[0],
			self.vertices[3],
			self.vertices[5],
			self.vertices[4]
		])
	@property
	def triangle_fan(self):
		return TriangleFan([
			self.center,
			self.vertices[0],
			self.vertices[1],
			self.vertices[2],
			self.vertices[3],
			self.vertices[4],
			self.vertices[5],
			self.vertices[0]
		])
	@property
	def triangles(self):
		return self.triangle_fan.triangles
		
	def draw(self):
		if self.selected:
			glColor3f(1.0,0.0,0.0)
		elif self.hover:
			glColor3f(0.0,0.0,1.0)
		else:
			glColor3f(1.0,1.0,1.0)
		self.triangle_fan.draw()

class D6Entity(RegularHexagon, ClickableObject):
	def __init__(self, vertex_count, center, radius, rotation_rad, layer):
		RegularHexagon.__init__(self, vertex_count, center, radius, rotation_rad, layer)
		ClickableObject.__init__(self)
		
if __name__ == "__main__":
	for triangle in RegularHexagon(6, coord.Coord(x=0.0,y=0.0), 1.0, 0.0, 0).triangle_strip.triangles:
		print(triangle)