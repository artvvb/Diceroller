from drawable import RegularHexagon
from clickable import ClickableObject

class DieEntity(RegularHexagon, ClickableObject):
	def __init__(self, die_side_count, center, radius, rotation_rad, layer):
		RegularPolygon.__init__(self, die_side_count, center, radius, rotation_rad, layer)
		ClickableObject.__init__(self)
	def draw(self):
		if self.selected:
			glColor3f(1.0,0.0,0.0)
		elif self.hover:
			glColor3f(0.0,0.0,1.0)
		else:
			glColor3f(1.0,1.0,1.0)
		RegularHexagon.draw(self)
