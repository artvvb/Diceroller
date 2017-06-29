from OpenGL.GL import glBegin
from OpenGL.GL import glEnd
from OpenGL.GL import glVertex2f
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

CONTAINMENT_OBJ = containment.BarycenterMethod()

class DrawableObject:
	def draw(self):
		glBegin(self.gl_property)
		for vertex in self.drawable_vertices: glVertex2f(vertex.x, vertex.y)
		glEnd()
	
class TriangleStrip(DrawableObject):
	@property
	def drawable_vertices(self):
		n = len(self.vertices)
		i,j = 0,1
		a = []
		while i != j:
			a.append(self.vertices[i])
			i = (i-1)%n
			a.append(self.vertices[j])
			if i == j: break
			j += 1
		return a
	@property
	def gl_property(self):
		return GL_TRIANGLE_STRIP
	@property
	def triangles(self):
		i = 0
		while i+2 < len(self.vertices):
			yield self.vertices[i:i+3]
			i += 1
			
class TriangleFan(DrawableObject):
	@property
	def drawable_vertices(self):
		yield self.center
		for vertex in self.vertices:
			yield vertex
		yield self.vertices[0]
		a = [self.center]
	@property
	def gl_property(self):
		return GL_TRIANGLE_FAN
	@property
	def triangles(self):
		i = 1
		while i+1 < len(self.vertices):
			yield [self.vertices[0], self.vertices[i], self.vertices[i+1]]
			i += 1
		
class RegularPolygon(TriangleFan):
	def __init__(self, vertex_count, center, radius, rotation_rad, layer):
		self.layer, self.center, self.vertex_count = layer, center, vertex_count
		base_vertex = self.center + coord.Coord(x=radius, y=0.0)
		base_vertex = rotate(base_vertex, self.center, rotation_rad)
		rad_between_vertices = 2*math.pi / vertex_count
		self.vertices = [rotate(base_vertex, self.center, x * rad_between_vertices) for x in range(vertex_count)]
		if TriangleFan in self.__class__.__bases__:
			TriangleFan.__init__(self)
		if TriangleStrip in self.__class__.__bases__:
			TriangleStrip.__init__(self)
	def contains(self, c):
		return CONTAINMENT_OBJ.any_triangles_contain(self.triangles, c)
	def rotate(self, rad):
		self.vertices = [rotate(vertex, self.center, rad) for vertex in self.vertices]
	def move(self, vec):
		self.center += vec
		self.vertices = [vertex + vec for vertex in self.vertices]
	def draw(self):
		if TriangleFan in self.__class__.__bases__:
			TriangleFan.draw(self)
		if TriangleStrip in self.__class__.__bases__:
			TriangleStrip.draw(self)
		