from vkbottle.bot import Bot
from vkbottle.bot import Message
from vkbottle import CtxStorage
from vkbottle import BaseStateGroup
from vkbottle import Keyboard, KeyboardButtonColor, Text, EMPTY_KEYBOARD

import asyncio
import urllib.request
import datetime
import loguru
import tool.config
import tool.wall
import tool.users_pay
import tool.post_date
import tool.payments
import time
import os

#loguru.logger.disable("vkbottle")
bot = Bot(token=tool.config.token_message)
ctx = CtxStorage()

users = tool.users_pay.UserPay()

class Create_post(BaseStateGroup):
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

	await message.answer(f"Привет, {user_name}.\nЯ Бот для создания и публикации рекламы в сообществе {tool.config.group_name}")
	time.sleep(2)
	await message.answer(f"Для того что бы продолжить тебе нужно написать или нажать на кнопку <Оплатить пост>", keyboard = keyboard)



@bot.on.private_message(text="Оплатить пост")
async def pay(message: Message):
	try:
		if users.get(user_id=message.from_id)[0] != "PAY":
			keyboard = Keyboard(inline=True)
			keyboard.add(Text("Проверить оплату"))

			await message.answer(f"Ссылка для оплаты: {tool.payments.quickpay(receiver=4100118153143687, sum_=300, label=message.from_id)}")
			users.set(user_id=message.from_id, param=["WAIT"])
		
			time.sleep(2)
			await message.answer("После оплаты нажмите кнопку ниже", keyboard=keyboard)
		else:
			keyboard = Keyboard(inline=True)
			keyboard.add(Text("Создать рекламный пост"))
			await message.answer("Ваш пост оплачен, давайте приступим к его созданию", keyboard=keyboard)
	except Exception:
		keyboard = Keyboard(inline=True)
		keyboard.add(Text("Проверить оплату"))

		await message.answer(f"Ссылка для оплаты: {tool.payments.quickpay(receiver=4100118153143687, sum_=300, label=message.from_id)}")
		users.set(user_id=message.from_id, param=["WAIT"])
		
		time.sleep(2)
		await message.answer("После оплаты нажмите кнопку ниже", keyboard=keyboard)



@bot.on.private_message(text="07")
async def pay(message: Message):
	users.set(user_id=message.from_id, param=["PAY"])



@bot.on.private_message(text="Проверить оплату")
async def pay(message: Message):
	if tool.payments.check_quickpay(user_id=message.from_id):
		users.set(user_id=message.from_id, param=["PAY"])
		
	if users.get(user_id=message.from_id)[0] == "PAY":
		keyboard = Keyboard(inline=True)
		keyboard.add(Text("Создать рекламный пост"))
		await message.answer("Ваш пост оплачен, давайте приступим к его созданию", keyboard=keyboard)
	
	else:
		await message.answer("Ваш пост не оплачен, пожалуйста оплатите или подождите пока сервис даст ответ и повторите попытку позже!")



@bot.on.private_message(lev="Создать рекламный пост")
async def create_post(message: Message):
	if users.get(user_id=message.from_id)[0] == "PAY":
		await message.answer("""
			Для легкого создания поста мы поделили это на этапы, пожалуйста соблюдайте правила иначе всё будет плохо!
			Если в каком-то шаге у вас отсутствует какой-то элемент то нажмите кнопку отстутствие
			
			1)Текст поста
			2)Прикрепления поста
			3)Дата публикации
			4)Ссылка на источник
			5)Закрытые коментарии
			""")
		keyboard = Keyboard(inline=True)
		keyboard.add(Text("Отсутствует"))
		await message.answer("Если элемент отсутствует нажмите кнопку ниже", keyboard=keyboard)
		await bot.state_dispenser.set(message.peer_id, Create_post.MESSAGE)
		return "Напишите текст поста"
	
	else:
		keyboard = Keyboard(inline=True)
		keyboard.add(Text("Оплатить пост"))

		await message.answer("Пожалуйста оплатите пост!", keyboard=keyboard)



@bot.on.private_message(state=Create_post.MESSAGE)
async def create_post(message: Message):
	ctx.set("message", message.text)

	keyboard = Keyboard(inline=True)
	keyboard.add(Text("Отсутствует"))
	await message.answer("Если элемент отсутствует нажмите кнопку ниже", keyboard=keyboard)
	await bot.state_dispenser.set(message.peer_id, Create_post.ATTACHMENTS)
	return "Прикрепите фотографии или видео"



@bot.on.private_message(state=Create_post.ATTACHMENTS)
async def create_post(message: Message):
	if message.text != "Отсутствует":
		attach = []

		if message.attachments:
			if message.attachments[0].photo:
				for i in range(len(message.attachments)):
					attach.append(f"photo{i}.png")
					urllib.request.urlretrieve(message.attachments[i].photo.sizes[-5].url, f"photo{i}.png")

				ctx.set("attachments", attach)
				await bot.state_dispenser.set(message.peer_id, Create_post.PUBLISH_DATE)
				return "Напишите время поста в формате гггг-мм-дд чч:мм:cc"
			
			elif message.attachments[0].video:
				pass
	else:
		ctx.set("attachments", "Отсутствует")
		await bot.state_dispenser.set(message.peer_id, Create_post.PUBLISH_DATE)
		return "Напишите время поста в формате гггг-мм-дд чч:мм:cc"



@bot.on.private_message(state=Create_post.PUBLISH_DATE)
async def create_post(message: Message):
	
	if tool.post_date.valid_date(publish_date=message.text) == -1:
		await bot.state_dispenser.set(message.peer_id, Create_post.PUBLISH_DATE)
		return "ошибка ввода даты, пожалуйста введите дату заного в формате гггг-мм-дд чч:мм:cc"
	

	elif tool.post_date.valid_date(publish_date=message.text) == 0:
		await bot.state_dispenser.set(message.peer_id, Create_post.PUBLISH_DATE)
		return "Введенная дата не может быть меньше текущей, пожалуйста введите дату заного в формате гггг-мм-дд чч:мм:cc"


	elif tool.post_date.valid_date(publish_date=message.text) == 1:
		ctx.set("publish_date", message.text)

		keyboard = Keyboard(inline=True)
		keyboard.add(Text("Отсутствует"))
		await message.answer("Если элемент отсутствует нажмите кнопку ниже", keyboard=keyboard)
		await bot.state_dispenser.set(message.peer_id, Create_post.REFERENCE)
		return "Пожалуйста укажите источник вашего поста"



@bot.on.private_message(state=Create_post.REFERENCE)
async def create_post(message: Message):
	ctx.set("reference", message.text)

	keyboard = Keyboard(inline=True)
	keyboard.add(Text("Да"))
	keyboard.row()
	keyboard.add(Text("Нет"))
	await message.answer("Для облегчения вот кнопки", keyboard=keyboard)
	await bot.state_dispenser.set(message.peer_id, Create_post.CLOSE_COMMENTS)
	return "Хотите ли вы закрыть комментарии в вашем посте?"



@bot.on.private_message(state=Create_post.CLOSE_COMMENTS)
async def create_post(message: Message):
	if message.text == "Да":
		ctx.set("close_comments", 1)
		await bot.state_dispenser.set(message.peer_id, Create_post.CONFIRM)
		return "Убедитесь что все данные введены правильно, иначе отменить действие не получится. Если готовы продолжить напишите Да, иначе Нет"

	
	elif message.text == "Нет":
		ctx.set("close_comments", 0)
		await bot.state_dispenser.set(message.peer_id, Create_post.CONFIRM)
		return "Убедитесь что все данные введены правильно, иначе отменить действие не получится. Если готовы продолжить напишите Да, иначе Нет"

	else:
		await message.answer("Не корректный ввод!")

		keyboard = Keyboard(inline=True)
		keyboard.add(Text("Да"))
		keyboard.row()
		keyboard.add(Text("Нет"))
		await message.answer("Для облегчения вот кнопки", keyboard=keyboard)
		await bot.state_dispenser.set(message.peer_id, Create_post.CLOSE_COMMENTS)
		return "Хотите ли вы закрыть комментарии в вашем посте?"



@bot.on.private_message(state=Create_post.CONFIRM)
async def create_post(message: Message):
	if message.text == "Да":
		# try:
		# 	await message.answer(str(ctx.get("message")))
		# 	await message.answer(str(ctx.get("attachments")))
		# 	await message.answer(str(ctx.get("publish_date")))
		# 	await message.answer(str(ctx.get("close_comments")))
		# 	await message.answer(str(ctx.get("reference")))
		# except Exception:
		# 	pass

		if ctx.get("message") == "Отсутствует" and ctx.get("attachments") == "Отсутствует":
			keyboard = Keyboard(inline=True)
			keyboard.add(Text("Отсутствует"))
			message.answer("Если элемент отсутствует нажмите кнопку ниже", keyboard=keyboard)

			await bot.state_dispenser.set(message.peer_id, Create_post.MESSAGE)
			return "Напишите текст поста"
		
		else:
			if ctx.get("message") == "Отсутствует":
				if ctx.get("reference") == "Отсутствует":
					tool.wall.post(
						attachments=ctx.get("attachments"),
						publish_date=datetime.datetime.strptime(ctx.get("publish_date"), "%Y-%m-%d %H:%M:%S"),
						close_comments = ctx.get("close_comments"),
					)
				else:
					tool.wall.post(
						attachments=ctx.get("attachments"),
						publish_date=datetime.datetime.strptime(ctx.get("publish_date"), "%Y-%m-%d %H:%M:%S"),
						close_comments = ctx.get("close_comments"),
						copyright=ctx.get("reference"),
					)

			if ctx.get("attachments") == "Отсутствует":
				if ctx.get("reference") == "Отсутствует":
					tool.wall.post(
						message=ctx.get("message"),
						publish_date=datetime.datetime.strptime(ctx.get("publish_date"), "%Y-%m-%d %H:%M:%S"),
						close_comments = ctx.get("close_comments"),
					)
				else:
					tool.wall.post(
						message=ctx.get("message"),
						publish_date=datetime.datetime.strptime(ctx.get("publish_date"), "%Y-%m-%d %H:%M:%S"),
						close_comments = ctx.get("close_comments"),
						copyright = ctx.get("reference"),
					)
			else:
				if ctx.get("reference") == "Отсутствует":
					tool.wall.post(
						message=ctx.get("message"),
						attachments=ctx.get("attachments"),
						publish_date=datetime.datetime.strptime(ctx.get("publish_date"), "%Y-%m-%d %H:%M:%S"),
						close_comments = ctx.get("close_comments"),
					)
				else:
					tool.wall.post(
						message=ctx.get("message"),
						attachments=ctx.get("attachments"),
						publish_date=datetime.datetime.strptime(ctx.get("publish_date"), "%Y-%m-%d %H:%M:%S"),
						close_comments = ctx.get("close_comments"),
						copyright = ctx.get("reference"),
					)

		await message.answer("Ваш пост занесен в список и во-время будет опубликован!")
		users.set(user_id=message.from_id, param=["WAIT", None])

		for item in ctx.get("attachments"):
			os.remove(item)
	
	elif message.text == "Нет":
		keyboard = Keyboard(inline=True)
		keyboard.add(Text("Создать рекламный пост"))
		await message.answer("Давайте приступим к созданию поста для этого нажмите кнопку ниже", keyboard=keyboard)

	else:
		await message.answer("Я тебя не понял, для того чтобы начать напиши Начать")



if __name__ == "__main__":
	bot.run_forever()