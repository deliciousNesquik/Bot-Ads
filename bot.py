from vkbottle.bot import Bot
from vkbottle.bot import Message
from vkbottle import CtxStorage
from vkbottle import BaseStateGroup
from vkbottle import Keyboard, KeyboardButtonColor, Text, EMPTY_KEYBOARD
from tools.customers import Customer

import asyncio
import urllib.request
import datetime
import loguru
import tools.config
import tools.wall
import tools.post_date
import tools.payments
import time
import os

bot = Bot(token=tools.config.token_message)
customers = Customer()
ctx = CtxStorage()

class PostCreator(BaseStateGroup):
    MESSAGE        = 1
    ATTACHMENTS    = 2
    PUBLISH_DATE   = 3
    REFERENCE      = 4
    CLOSE_COMMENTS = 5
    CONFIRM        = 6



@bot.on.private_message(text="Начать")
async def start(message: Message):
	users_info = await bot.api.users.get(message.from_id)
	user_name = users_info[0].first_name + " " + users_info[0].last_name
	
	keyboard = Keyboard(inline=True)
	keyboard.add(Text("Оплатить пост"))
	
	await message.answer(f"""
Привет, {user_name}.\nЯ Бот для создания и публикации рекламы в сообществе:
{tools.config.group_name}.

Для того чтобы продолжить нужно оплатить пост, стоимость фиксирована -{tools.config.price_ads}₽, просто нажмите кнопку ниже""",
keyboard=keyboard
)



@bot.on.private_message(text="Оплатить пост")
async def pay(message: Message):
	
	if len(customers.get(user_id=message.from_id)) > 0 and customers.get(user_id=message.from_id)[0] == "PAY":
		keyboard = Keyboard(inline=True)
		keyboard.add(Text("Создать рекламный пост"))
		
		await message.answer("Ваш пост оплачен, давайте приступим к его созданию", keyboard=keyboard)

	else:
		keyboard = Keyboard(inline=True)
		keyboard.add(Text("Проверить оплату"))

		customers.set(user_id=message.from_id, param=["WAIT", tools.payments.generate_label()])
		paying = tools.payments.quickpay(
					receiver=tools.config.receiver,
					sum_=tools.config.price_ads,
					label=customers.get(message.from_id)[1],
				)
		await message.answer(f"Ссылка для оплаты: {paying}"); time.sleep(1)
		await message.answer("После оплаты нажмите кнопку ниже", keyboard=keyboard)



@bot.on.private_message(text="1")
async def pay(message: Message):
	customers.ins(user_id=message.from_id, param="PAY", index=0)



@bot.on.private_message(text="Проверить оплату")
async def pay(message: Message):
	if tools.payments.check_quickpay(label=customers.get(message.from_id)[1]):
		customers.set(user_id=message.from_id, param=["PAY"])
		
	if customers.get(user_id=message.from_id)[0] == "PAY":
		keyboard = Keyboard(inline=True)
		keyboard.add(Text("Создать рекламный пост"))
		await message.answer("Ваш пост оплачен, давайте приступим к его созданию", keyboard=keyboard)
	
	else:
		await message.answer("Ваш пост не оплачен, пожалуйста оплатите или подождите пока сервис даст ответ и повторите попытку позже!")



@bot.on.private_message(lev="Создать рекламный пост")
async def create_post(message: Message):
	if len(customers.get(user_id=message.from_id)) > 0 and customers.get(user_id=message.from_id)[0] == "PAY":
		await message.answer("""
Создание рекламного поста делится на некоторые этапы, в некоторых из них вы можете выбрать отсутствие элемента, для этого просто нажмите кнопку (Отсутствует)

1)Сообщение поста
2)Прикрепления поста
3)Дата публикации поста
4)Ссылка на источник
5)Закрытые коментарии поста""")

		keyboard = Keyboard(inline=True)
		keyboard.add(Text("Отсутствует"))
		await bot.state_dispenser.set(message.peer_id, PostCreator.MESSAGE)
		return await message.answer("Введите сообщение поста:", keyboard=keyboard)
		
	else:
		keyboard = Keyboard(inline=True)
		keyboard.add(Text("Оплатить пост"))

		await message.answer("Для создания рекламного поста его необходимо оплатить!", keyboard=keyboard)



@bot.on.private_message(state=PostCreator.MESSAGE)
async def create_post(message: Message):
	customers.add(message.from_id, message.text)
	ctx.set("message", message.text)

	keyboard = Keyboard(inline=True)
	keyboard.add(Text("Отсутствует"))
	await bot.state_dispenser.set(message.peer_id, PostCreator.ATTACHMENTS)
	return await message.answer("Прикрепите фотографии или видео", keyboard=keyboard)



@bot.on.private_message(state=PostCreator.ATTACHMENTS)
async def create_post(message: Message):
	if message.text != "Отсутствует":
		attach = []

		if message.attachments:
			if message.attachments[0].photo:
				for i in range(len(message.attachments)):
					attach.append(f"photo{i}.png")
					urllib.request.urlretrieve(message.attachments[i].photo.sizes[-5].url, f"photo{i}.png")

				ctx.set("attachments", attach)
				customers.add(message.from_id, attach)
				await bot.state_dispenser.set(message.peer_id, PostCreator.PUBLISH_DATE)
				return await message.answer("Напишите время поста в формате гггг-мм-дд чч:мм")
			
			elif message.attachments[0].video:
				for i in range(len(message.attachments)):
					attach.append(f"video{i}.mp4")
					urllib.request.urlretrieve(message.attachments[i].video.url, f"video{i}.mp4")

				ctx.set("attachments", attach)
				customers.add(message.from_id, attach)
				await bot.state_dispenser.set(message.peer_id, PostCreator.PUBLISH_DATE)
				return await message.answer("Напишите время поста в формате гггг-мм-дд чч:мм")
	else:
		ctx.set("attachments", "Отсутствует")
		customers.add(message.from_id, "Отсутствует")
		if ctx.get("message") == "Отсутствует" and ctx.get("attachments") == "Отсутствует":
			await message.answer("Вы допустили ошибку! Сообщение поста или фотографии должны быть заполнены!")
			time.sleep(2)

			keyboard = Keyboard(inline=True)
			keyboard.add(Text("Отсутствует"))

			await bot.state_dispenser.set(message.peer_id, PostCreator.MESSAGE)
			return await message.answer("Введите сообщение поста:", keyboard=keyboard)
		else:
			await bot.state_dispenser.set(message.peer_id, PostCreator.PUBLISH_DATE)
			return await message.answer("Напишите время поста в формате гггг-мм-дд чч:мм")



@bot.on.private_message(state=PostCreator.PUBLISH_DATE)
async def create_post(message: Message):
	
	if tools.post_date.valid_date(publish_date=message.text) == -1:
		await bot.state_dispenser.set(message.peer_id, PostCreator.PUBLISH_DATE)
		return await message.answer("ошибка ввода даты, пожалуйста введите дату заного в формате гггг-мм-дд чч:мм")
		

	elif tools.post_date.valid_date(publish_date=message.text) == 0:
		await bot.state_dispenser.set(message.peer_id, PostCreator.PUBLISH_DATE)
		return await message.answer("Введенная дата не может быть меньше текущей, пожалуйста введите дату заного в формате гггг-мм-дд чч:мм")


	elif tools.post_date.valid_date(publish_date=message.text) == 1:
		if tools.post_date.date_is_free(date_to_check=message.text+":00") == 1:
			ctx.set("publish_date", message.text+":00")
			customers.add(message.from_id, message.text+":00")

			keyboard = Keyboard(inline=True)
			keyboard.add(Text("Отсутствует"))
			await bot.state_dispenser.set(message.peer_id, PostCreator.REFERENCE)
			return await message.answer("Пожалуйста укажите источник вашего поста", keyboard=keyboard)
		elif tools.post_date.date_is_free(date_to_check=message.text+":00") == 0:
			await bot.state_dispenser.set(message.peer_id, PostCreator.PUBLISH_DATE)
			return await message.answer("Введенная дата занята, пожалуйста введите другую дату с интервалом в 3 часа или больше")
		elif tools.post_date.date_is_free(date_to_check=message.text+":00") == -1:
			await bot.state_dispenser.set(message.peer_id, PostCreator.PUBLISH_DATE)
			return await message.answer("На данный день закончились записи, попробуйте ввести другой день")



@bot.on.private_message(state=PostCreator.REFERENCE)
async def create_post(message: Message):
	ctx.set("reference", message.text)
	customers.add(message.from_id, message.text)

	keyboard = Keyboard(inline=True)
	keyboard.add(Text("Да"))
	keyboard.row()
	keyboard.add(Text("Нет"))
	await bot.state_dispenser.set(message.peer_id, PostCreator.CLOSE_COMMENTS)
	return await message.answer("Хотите ли вы закрыть комментарии в вашем посте?", keyboard=keyboard)



@bot.on.private_message(state=PostCreator.CLOSE_COMMENTS)
async def create_post(message: Message):
	if message.text == "Да":
		ctx.set("close_comments", 1)
		customers.add(message.from_id, 1)
		keyboard = Keyboard(inline=True)
		keyboard.add(Text("Да"))
		keyboard.row()
		keyboard.add(Text("Нет"))

		await bot.state_dispenser.set(message.peer_id, PostCreator.CONFIRM)
		return await message.answer("Убедитесь что все данные введены правильно, иначе отменить действие не получится. Если готовы продолжить нажмите Да, иначе Нет", keyboard=keyboard)

	
	elif message.text == "Нет":
		ctx.set("close_comments", 0)
		customers.add(message.from_id, 0)
		keyboard = Keyboard(inline=True)
		keyboard.add(Text("Да"))
		keyboard.row()
		keyboard.add(Text("Нет"))

		await bot.state_dispenser.set(message.peer_id, PostCreator.CONFIRM)
		return await message.answer("Убедитесь что все данные введены правильно, иначе отменить действие не получится. Если готовы продолжить нажмите Да, иначе Нет", keyboard=keyboard)

	else:
		await message.answer("Не корректный ввод!")
		await bot.state_dispenser.set(message.peer_id, PostCreator.CLOSE_COMMENTS)
		return await message.answer("Хотите ли вы закрыть комментарии в вашем посте?", keyboard=keyboard)


@bot.on.private_message(state=PostCreator.CONFIRM)
async def create_post(message: Message):
	if message.text == "Да":

		if customers.get(message.from_id)[1] == "Отсутствует" and customers.get(message.from_id)[2] == "Отсутствует":
			await message.answer("Вы допустили ошибку! Сообщение поста или фотографии должны быть заполнены!")
			time.sleep(2)


			keyboard = Keyboard(inline=True)
			keyboard.add(Text("Отсутствует"))

			await bot.state_dispenser.set(message.peer_id, PostCreator.MESSAGE)
			return await message.answer("Введите сообщение поста:", keyboard=keyboard)
		
		else:
			if customers.get(message.from_id)[1] == "Отсутствует":
				if customers.get(message.from_id)[4] == "Отсутствует":
					tools.wall.post(
						attachments    =customers.get(message.from_id)[2],
						publish_date   =datetime.datetime.strptime(customers.get(message.from_id)[3], "%Y-%m-%d %H:%M:%S"),
						close_comments =customers.get(message.from_id)[5],
					)
				else:
					tools.wall.post(
						attachments    = customers.get(message.from_id)[2],
						publish_date   = datetime.datetime.strptime(customers.get(message.from_id)[3], "%Y-%m-%d %H:%M:%S"),
						close_comments = customers.get(message.from_id)[5],
						copyright      = customers.get(message.from_id)[4],
					)

			if customers.get(message.from_id)[2] == "Отсутствует":
				if customers.get(message.from_id)[4] == "Отсутствует":
					tools.wall.post(
						message        = customers.get(message.from_id)[1],
						publish_date   = datetime.datetime.strptime(customers.get(message.from_id)[3], "%Y-%m-%d %H:%M:%S"),
						close_comments = customers.get(message.from_id)[5],
					)
				else:
					tools.wall.post(
						message        = customers.get(message.from_id)[1],
						publish_date   = datetime.datetime.strptime(customers.get(message.from_id)[3], "%Y-%m-%d %H:%M:%S"),
						close_comments = customers.get(message.from_id)[5],
						copyright      = customers.get(message.from_id)[4],
					)
			else:
				if customers.get(message.from_id)[4] == "Отсутствует":
					tools.wall.post(
						message        = customers.get(message.from_id)[1],
						attachments    = customers.get(message.from_id)[2],
						publish_date   = datetime.datetime.strptime(customers.get(message.from_id)[3], "%Y-%m-%d %H:%M:%S"),
						close_comments = customers.get(message.from_id)[5],
					)
				else:
					tools.wall.post(
						message        = customers.get(message.from_id)[1],
						attachments    = customers.get(message.from_id)[2],
						publish_date   = datetime.datetime.strptime(customers.get(message.from_id)[3], "%Y-%m-%d %H:%M:%S"),
						close_comments = customers.get(message.from_id)[5],
						copyright      = customers.get(message.from_id)[4],
					)

		await message.answer("Ваш пост занесен в список и вовремя будет опубликован!")

		if customers.get(message.from_id)[2] != "Отсутствует":
			for item in customers.get(message.from_id)[2]:
				os.remove(item)

		customers.set(user_id=message.from_id, param=["WAIT"])
	
	elif message.text == "Нет":
		keyboard = Keyboard(inline=True)
		keyboard.add(Text("Создать рекламный пост"))
		await message.answer("Давайте приступим к созданию поста для этого нажмите кнопку ниже", keyboard=keyboard)

	else:
		keyboard = Keyboard(inline=True)
		keyboard.add(Text("Создать рекламный пост"))
		await message.answer("Я тебя не понял", keyboard=keyboard)



if __name__ == "__main__":
	bot.run_forever()