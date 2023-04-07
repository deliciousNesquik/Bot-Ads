from vk_api import VkApi

def _auth_handler() -> int and bool:
	key = input("Введите ключ двуфакторной аутефикации: ")
	remember_device = True

	return key, remember_device

def _authorization(token: str) -> VkApi:
	try:
		session = VkApi(token=token)
		return session.get_api()

	except Exception as ex:
		return ex