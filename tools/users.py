class User():
	# users = {
	# 	'45637647': ["PAY", label, message, attachments, publish_date, reference, close_comments]
	#				   0       1      2          3            4             5           6
	# }

	def __init__(self):
		self.users = {}

	def add(self, user_id: int, param: str):
		self.users[user_id].append(param)

	def set(self, user_id: int, param: list):
		self.users[user_id] = param

	def get(self, user_id: int):
		return self.users.get(user_id)

	def rem(self, user_id: int):
		del self.users[user_id]