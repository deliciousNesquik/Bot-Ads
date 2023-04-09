
"""
------------------------------------------------------------------------
Данные группы Помощник | Бот Уат
"""
owner_id   = 210049982 			 			  #id группы
group_name = "Помощник | Бот Уат" 			  #название группы
price_ads  = 300 				  			  #цена одной рекламы
admins_id = [469440405, 751135793, 386729911] #id админов группы

#токены для стены, сообщений, оплаты
token_wall = ""
token_message = ""
token_payments = ""

#данные от приложения yoomoney 
client_id = ""										  #id приложения
redirect_uri = "https://vk.com/mambastikfantastik"																	  #ссылка переадресации
scope=["account-info", "operation-history", "operation-details", "incoming-transfers", "payment-p2p", "payment-shop"] #права для приложения


"""
-----------------------------------------------------------------------
Настройки, переменные для бота и других модулей
"""
path_json = "data/posts.json" 					#путь к файлу с постами
path_log = "data/log/log.txt" 					#путь к файлу с логами
path_db = "data/customers.db"					#путь к файлу с базой данных
photo_expansion = ['png', 'jpg', 'jpeg', 'gif'] #расширения для фото
video_expansion = ['mp4', 'avi'] 				#расширения для видео