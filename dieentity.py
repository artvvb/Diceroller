from drawable import RegularPolygon
from clickable import ClickableObject

def dummy_update(obj):
	pass
	
class DieEntity(RegularPolygon, ClickableObject):
	def __init__(self, die_side_count, center, radius, rotation_rad, layer):
		RegularPolygon.__init__(self, die_side_count, center, radius, rotation_rad, layer)
		ClickableObject.__init__(self)
		update = dummy_update
	def draw(self):
		ClickableObject.draw(self)
		RegularPolygon.draw(self)
	def set_update(self, update):
		self.update = update
	def rotate(self, rad):
		RegularPolygon.rotate(self, rad)
	def move(self, vec):
		RegularPolygon.move(self, vec)
		
		