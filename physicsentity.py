import coord
class PhysicsEntity:
	def __init__(self, velocity, position, acceleration, angular_offset, angular_speed):
		self.velocity, self.position, self.acceleration = velocity, position, acceleration, 
		self.angular_offset, self.angular_speed = angular_offset, angular_speed
	def update(self):
		if self.is_enabled:
			# discrete function, should integrate over path
			self.position += self.velocity
			self.velocity += self.acceleration
			self.angular_offset += self.angular_speed
			
class RotationalEntity:
	def __init__(self, angular_velocity, angular_position):
		self.angular_velocity, self.angular_position = angular_velocity, angular_position
		self.mvec2av = 0.1
	def apply_force(self, location, vector):
		if location == self.center: return
		#radius = magnitude(self.center - location)
		#delta_angular_velocity = vector_component_tangential_to_radius into angular_velocity
		#self.angular_velocity += delta_angular_velocity
	def update(self):
		self.angular_position += self.angular_velocity
		
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
		