from yoomoney import Authorize
from yoomoney import Client
from yoomoney import Quickpay
from . import config


import string
import random
import config

# client_id="B7C9434ABCF05D493893D03C16BEAFD638BC900828454D0C30D37BD5A94E9A9B"
# redirect_uri="https://vk.com/uatbot"
# scope=["account-info"
#        "operation-history"
#        "operation-details"
#        "incoming-transfers"
#        "payment-p2p"
#        "payment-shop"
#4100118153143687.5C0405BF25E44000DDEF7964FEAFD9A9C25EC9020AEEAEC228FB4A48179AFA731F740947DFC037E620DFAEA33F4770A16CE17B782BE281BDAEDD6C43847BFC489B6A15A1E3F7CA67CE44F5F40DB6A72F73159D7771B99ED37EF5135F09A18A761C10BA5FC3C7BF76DCC10778091B36B2D478C7F982E034B7B95D3EEE99E4A4B8

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


# client_id="B7C9434ABCF05D493893D03C16BEAFD638BC900828454D0C30D37BD5A94E9A9B"
# redirect_uri="https://vk.com/uatbot"
# scope=["account-info"
#        "operation-history"
#        "operation-details"
#        "incoming-transfers"
#        "payment-p2p"
#        "payment-shop"
#4100118153143687.5C0405BF25E44000DDEF7964FEAFD9A9C25EC9020AEEAEC228FB4A48179AFA731F740947DFC037E620DFAEA33F4770A16CE17B782BE281BDAEDD6C43847BFC489B6A15A1E3F7CA67CE44F5F40DB6A72F73159D7771B99ED37EF5135F09A18A761C10BA5FC3C7BF76DCC10778091B36B2D478C7F982E034B7B95D3EEE99E4A4B8

if __name__ == "__main__":
	pay = Payment(
		client_id="B7C9434ABCF05D493893D03C16BEAFD638BC900828454D0C30D37BD5A94E9A9B", 
		redirect_uri="https://vk.com/uatbot", 
		scope=["account-info",
       			"operation-history",
       			"operation-details",
       			"incoming-transfers",
       			"payment-p2p",
       			"payment-shop",
       		]
       	)