from yoomoney import Authorize
from yoomoney import Client
from yoomoney import Quickpay

global token
token = "4100118153143687.F73F740B5617374115ADC5A7653EF0B1FE1E6A08076B16482702B2CF3E5E8665EF4EF2962CA87C62F28189C761D84C3819548B790811F35C1E8340D1F3339DFA00190134299A66B311287E4BDC1D39E8BB091E183BCB3A1654010253D12953C938BFE83F7BC43EFAF9079E7B7A76B8A6C8D53F57CCE113D520D2FAB35B993DD1"

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


#216C5EF95627E39FFE3C7D346013BC944607426EAD284FD42433F3CDA203813970FD9B6FA59C7B16F379B409B6AAFFD93DB1CD287F2363823A72ECD9A957A321341FC7AE3AD0B79E8A84D9B38B393D614BB65ABD026A72F757E3EEE110C5BEC515C4D9957DD4F68147741FCD20B4819E0550E6798FA84C992533B2335815C12E

#token: 4100118153143687.F73F740B5617374115ADC5A7653EF0B1FE1E6A08076B16482702B2CF3E5E8665EF4EF2962CA87C62F28189C761D84C3819548B790811F35C1E8340D1F3339DFA00190134299A66B311287E4BDC1D39E8BB091E183BCB3A1654010253D12953C938BFE83F7BC43EFAF9079E7B7A76B8A6C8D53F57CCE113D520D2FAB35B993DD1

# token = Authorize(
# 	client_id="B7C9434ABCF05D493893D03C16BEAFD638BC900828454D0C30D37BD5A94E9A9B",
# 	redirect_uri="https://vk.com/uatbot",
# 	scope=["account-info",
# 			"operation-history",
# 			"operation-details",
# 			"incoming-transfers",
# 			"payment-p2p",
# 			"payment-shop",
# 		]
#     )
# client = Client(token)
# user = client.account_info()
# print("Account number:", user.account)
# print("Account balance:", user.balance)
# print("Account currency code in ISO 4217 format:", user.currency)
# print("Account status:", user.account_status)
# print("Account type:", user.account_type)
# print("Extended balance information:")

# quickpay = Quickpay(
#             receiver="4100118153143687",
#             quickpay_form="shop",
#             targets="Sponsor this project",
#             paymentType="SB",
#             sum=150,
#             label="a1b2c3d4e5"
#             )
# print(quickpay.base_url)
# print(quickpay.redirected_url)

