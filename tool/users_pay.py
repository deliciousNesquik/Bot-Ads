class UserPay():

	def __init__(self):
		self.users = {}

	def set(self, user_id: int, param: list):
		self.users[user_id] = param

	def get(self, user_id: int):
		return self.users.get(user_id)