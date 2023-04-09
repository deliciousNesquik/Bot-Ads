from vk_api import VkTools

class Tools():
	def __init__(self, session):
		self.tools = VkTools(session)

	def get_tools(self):
		return self.tools