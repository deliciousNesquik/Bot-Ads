from yoomoney import Authorize
from yoomoney import Client
from yoomoney import Quickpay
from . import config

import string
import random
import config

class Payment():
	def __init__(self, client_id:str, redirect_uri:str, scope:list) -> bool:
		try:
			self.token = Authorize(client_id=client_id, redirect_uri=redirect_uri, scope=scope)
			self.client = Client(self.token)
			self.user_info = self.client.account_info()
			self.receiver = self.user_info.account
		except Exception:
			pass
		

	def generate_label() -> str:
		chars = string.ascii_letters + string.digits
		label = ''.join(random.choice(chars) for _ in range(5))
		return label


	def quickpay(sum_: int, label: int):
		return Quickpay(
				receiver=self.receiver,
				quickpay_form=config.group_name,
				targets="Реклама в сообществе вконтакте",
				paymentType="SB",
				label=label,
				sum=sum_,
				).redirected_url


	def check_quickpay(label: int) -> bool:
		history = self.client.operation_history(label=label)

		for operation in history.operations:
			if operation.status == "success" and operation.amount == config.price_ads:
				return True


def generate_label() -> str:
    chars = string.ascii_letters + string.digits
    label = ''.join(random.choice(chars) for _ in range(5))
    return label


def quickpay(receiver: int, sum_: int, label: int):
	return Quickpay(
            receiver=receiver,
            quickpay_form="shop",
            targets="ads",
            paymentType="SB",
            label=label,
            sum=sum_,
            ).redirected_url


def check_quickpay(label: int) -> bool:
	client = Client(config.token_payments)
	history = client.operation_history(label=label)

	for operation in history.operations:
		if operation.status == "success" and operation.amount == 300:
			return True


