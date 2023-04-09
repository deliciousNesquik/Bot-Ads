from vk_api import VkApi

class Authorization():
	# def _auth_handler() -> int and bool:
	# 	key = input("Введите ключ двуфакторной аутефикации: ")
	# 	remember_device = True

	# 	return key, remember_device

	def __init__(self, token=None, login=None, password=None):
		self.session = VkApi(token=token)


	def get_api(self):
		return self.session.get_api()