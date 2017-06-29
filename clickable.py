from OpenGL.GL import glColor3f

class ClickableObject():
	def __init__(self):
		self.selected = False
		self.hover = False
	def select(self, new_center):
		self.center = new_center
		self.selected = True
	def deselect(self):
		self.selected = False
	def draw(self):
		if self.selected:
			glColor3f(1.0,0.0,0.0)
		elif self.hover:
			glColor3f(0.0,0.0,1.0)
		else:
			glColor3f(1.0,1.0,1.0)