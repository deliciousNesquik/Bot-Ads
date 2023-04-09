from yoomoney import Authorize
from yoomoney import Client
from yoomoney import Quickpay
from . import config


import string
import random
# import config



class Payment():
	def __init__(self, token:str=None, client_id:str=None, redirect_uri:str=None, scope:list=None) -> bool:
		if token is None:
			try:
				self.token = Authorize(client_id=client_id, redirect_uri=redirect_uri, scope=scope)
				self.client = Client(self.token)
				self.user_info = self.client.account_info()
				self.receiver = self.user_info.account
			except Exception:
				pass
		else:
			self.token = token
			self.client = Client(self.token)
			self.user_info = self.client.account_info()
			self.receiver = self.user_info.account

	def get_token(self):
		return self.token

	def generate_label(self) -> str:
		chars = string.ascii_letters + string.digits
		label = ''.join(random.choice(chars) for _ in range(5))
		return label

	def quickpay(self, sum_: int, label: int):
		return Quickpay(
				receiver=str(self.receiver),
				quickpay_form="shop",
				targets="Реклама в сообществе вконтакте",
				paymentType="SB",
				label=label,
				sum=sum_,
				).base_url

	def check_quickpay(self, label: int) -> bool:
		history = self.client.operation_history(label=label)

		for operation in history.operations:
			if operation.status == "success":
				return True

# if __name__ == "__main__":
# 	#payment = Payment(client_id=config.client_id, redirect_uri=config.redirect_uri, scope=config.scope)
# 	payment = Payment(token=config.token_payments)
# 	label = payment.generate_label()
# 	print(payment.quickpay(sum_=300, label=label))