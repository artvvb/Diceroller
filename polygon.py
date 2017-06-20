from OpenGL.GL import *
import coord
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
	
class RegularPolygon:
	def __init__(self, vertex_count, center, radius, rotation_rad, layer):
		self.layer, self.center = layer, center
		update = dummy_update
		base_vertex = self.center + coord.Coord(x=radius, y=0.0)
		base_vertex = rotate(base_vertex, self.center, rotation_rad)
		rad_between_vertices = 2*math.pi / vertex_count
		self.vertices = [rotate(base_vertex, self.center, x * rad_between_vertices) for x in range(vertex_count)]
	def set_update(self, update):
		self.update = update
	def draw(self):
		glBegin(GL_POLYGON)
		glColor3f(1.0,1.0,1.0)
		for vertex in self.vertices: glVertex2f(vertex.x, vertex.y)
		glEnd()
	def rotate(self, rad):
		print(rad)
		self.vertices = [rotate(vertex, self.center, rad) for vertex in self.vertices]
	def move(self, vec):
		self.center += vec
		self.vertices = [vertex + vec for vertex in self.vertices]