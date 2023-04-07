class Customer():
	"""Хранение данных:
	словарь = {
		id_пользователя: [
			"PAY" - статус оплаты, индекс 0
			"Label" - метка оплаты, идекс 1
			"Message" - сообщение, индекс 2
			"Attachments" - прикрепления, индекс 3
			"Publish_date" - время поста, индкес 4
			"Reference" - ссылка на источник, индекс 5
			"Close_comments" - закрытые комментарии, индекс 6
		]
	}
	
	__init__
	при создании класса создается словарь пользователей

	add
	добавляет переданный аргумент в конец списка аргументов пользователя

	set
	устанавливает переданный аргумент как список аргументов для пользователя

	ins
	вставляет переданный аргумент в нужное место для переданного пользователя

	get
	возращает список аргументов для переданного пользователя

	rem
	удаляет переданного пользователя из словаря
	"""

	def __init__(self):
		self.users = {}

	def add(self, user_id: int, param: str):
		self.users[user_id].append(param)

	def set(self, user_id: int, param: list):
		self.users[user_id] = param

	def ins(self, user_id: int, param:str, index: int):
		self.users[user_id][index] = param

	def get(self, user_id: int):
		if (self.users.get(user_id)) is None:
			self.users[user_id] = []
			return self.users[user_id]
		else:
			return self.users[user_id]

	def rem(self, user_id: int):
		del self.users[user_id]

# if __name__ == "__main__":
# 	customers = Customer()
# 	customers.set(user_id=1, param=["PAY", "1323123"])


# 	if len(customers.get(user_id=1)) > 0 and customers.get(user_id=1)[0] == "PAY":
# 		print(1)
# 	else:
# 		customers.set(user_id=1, param=["WAIT", "1323123"])
# 		print(2)