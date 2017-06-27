import coord
class PhysicsEntity:
	def __init__(self, velocity, position, acceleration, angular_offset, angular_speed):
		self.velocity, self.position, self.acceleration = velocity, position, acceleration, 
	def update(self):
		if self.is_enabled:
			# discrete function, should integrate over path
			self.position += self.velocity
			self.velocity += self.acceleration
	def enable(self):
		self.is_enabled = True
	def disable(self):
		self.is_enabled = False
	def next(self):
		
		
# use self.vertices to calculate collision
class CollisionMethod:
	def __init__(self):
		pass
	def check_collision(self, object1, object2):
		# return point of impact (if any) and vector normal to collision
		pass
		
class BoolCollisionMethod:
	def __init__(self):
		pass
	def will_collide(self, object1, object2):
		# an entity contains a bounding box described by a vertex list, 
	def has_collided(self, object1, object2):
		