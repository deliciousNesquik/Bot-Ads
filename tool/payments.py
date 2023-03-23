from yoomoney import Authorize
from yoomoney import Client
from yoomoney import Quickpay

global token
token = ""

def quickpay(receiver: int, sum_: int, label: int):
	return Quickpay(
            receiver=receiver,
            quickpay_form="shop",
            targets="ads",
            paymentType="SB",
            label=user_id,
            sum=sum_,
            ).redirected_url

def check_quickpay(user_id: int) -> bool:
	global token
	client = Client(token)
	history = client.operation_history(label=user_id)

	for operation in history.operations:
		if operation.status == "success" and operation.amount == 300:
			return True
