from vkbottle.bot import Bot
from vkbottle.bot import Message
from vkbottle import CtxStorage
from vkbottle import BaseStateGroup
from vkbottle import Keyboard, KeyboardButtonColor, Text, EMPTY_KEYBOARD
from tools.customers import Customer
from tools.payments import Payment
from tools.sql import DataBase

import asyncio
import urllib.request
import datetime
import loguru
import tools.config
import tools.wall
import tools.post_date
import tools.log_tools
import tools.json_tools
import time
import os

#loguru.logger.disable("vkbottle")
db        = DataBase(tools.config.path_db)
bot       = Bot(token=tools.config.token_message)
ctx       = CtxStorage()
payment   = Payment(token=tools.config.token_payments)
customers = Customer()

class PostCreator(BaseStateGroup):
    CONTENT        = 1
    PUBLISH_DATE   = 2
    REFERENCE      = 3
    CLOSE_COMMENTS = 4
    CONFIRM        = 5


@bot.on.private_message(text="Начать")
async def start(message: Message):
	users_info = await bot.api.users.get(message.from_id)
	user_name = users_info[0].first_name + " " + users_info[0].last_name
	tools.log_tools.logging(log_file=tools.config.path_log, string = f"[bot][info]Пользователь {user_name} действие <Начал переписку>", time=datetime.datetime.now(), limit=10)
	
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
	users_info = await bot.api.users.get(message.from_id)
	user_name = users_info[0].first_name + " " + users_info[0].last_name
	tools.log_tools.logging(log_file=tools.config.path_log, string = f"[bot][info]Пользователь {user_name} действие <Начал оплату>", time=datetime.datetime.now(), limit=10)

	if len(customers.get(user_id=message.from_id)) > 0 and customers.get(user_id=message.from_id)[0] == "PAY":
		tools.log_tools.logging(log_file=tools.config.path_log, string = f"[bot][info]Пользователь {user_name} действие <Оплатил пост>", time=datetime.datetime.now(), limit=10)
		keyboard = Keyboard(inline=True)
		keyboard.add(Text("Создать рекламный пост"))

		await message.answer("Ваш пост оплачен, давайте приступим к его созданию", keyboard=keyboard)

	else:
		keyboard = Keyboard(inline=True)
		keyboard.add(Text("Проверить оплату"))

		customers.set(user_id=message.from_id, param=["WAIT", payment.generate_label()])
		ref = payment.quickpay(
					sum_=tools.config.price_ads,
					label=customers.get(message.from_id)[1],
				)
		await message.answer(f"Ссылка для оплаты: {ref}"); time.sleep(1)
		await message.answer("После оплаты нажмите кнопку ниже", keyboard=keyboard)



@bot.on.private_message(text="1")
async def pay(message: Message):
	customers.ins(user_id=message.from_id, param="PAY", index=0)



@bot.on.private_message(text="Проверить оплату")
async def pay(message: Message):
	users_info = await bot.api.users.get(message.from_id)
	user_name = users_info[0].first_name + " " + users_info[0].last_name
	if payment.check_quickpay(label=customers.get(message.from_id)[1]):
		customers.set(user_id=message.from_id, param=["PAY"])
		
	if customers.get(user_id=message.from_id)[0] == "PAY":
		tools.log_tools.logging(log_file=tools.config.path_log, string = f"[bot][info]Пользователь {user_name} действие <Оплатил пост>", time=datetime.datetime.now(), limit=10)
		keyboard = Keyboard(inline=True)
		keyboard.add(Text("Создать рекламный пост"))
		await message.answer("Ваш пост оплачен, давайте приступим к его созданию", keyboard=keyboard)
	
	else:
		await message.answer("Ваш пост не оплачен, пожалуйста оплатите или подождите пока сервис даст ответ и повторите попытку позже!")



@bot.on.private_message(lev="Создать рекламный пост")
async def create_post(message: Message):
	users_info = await bot.api.users.get(message.from_id)
	user_name = users_info[0].first_name + " " + users_info[0].last_name
	if len(customers.get(user_id=message.from_id)) > 0 and customers.get(user_id=message.from_id)[0] == "PAY":
		tools.log_tools.logging(log_file=tools.config.path_log, string = f"[bot][info]Пользователь {user_name} действие <Начал создание поста>", time=datetime.datetime.now(), limit=10)
		await message.answer("""
Создание рекламного поста делится на некоторые этапы, в некоторых из них вы можете выбрать отсутствие элемента, для этого просто нажмите кнопку (Отсутствует)

1)Контент поста (фотографий 3 шт. макс.| видео не поддерживает)
3)Дата публикации поста
4)Ссылка на источник
5)Закрытые коментарии поста""")

		await bot.state_dispenser.set(message.peer_id, PostCreator.CONTENT)
		return await message.answer("Введите контент поста:")
		
	else:
		keyboard = Keyboard(inline=True)
		keyboard.add(Text("Оплатить пост"))

		await message.answer("Для создания рекламного поста его необходимо оплатить!", keyboard=keyboard)



@bot.on.private_message(state=PostCreator.CONTENT)
async def create_post(message: Message):
	users_info = await bot.api.users.get(message.from_id)
	user_name = users_info[0].first_name + " " + users_info[0].last_name

	if message.text:
		tools.log_tools.logging(log_file=tools.config.path_log, string = f"[bot][info]Пользователь {user_name} действие <Ввел сообщение>", time=datetime.datetime.now(), limit=10)
		customers.add(message.from_id, message.text)
		ctx.set("content", message.text)
	else:
		tools.log_tools.logging(log_file=tools.config.path_log, string = f"[bot][info]Пользователь {user_name} действие <Не ввел сообщение>", time=datetime.datetime.now(), limit=10)
		customers.add(message.from_id, None)
		ctx.set("content", None)

	if message.attachments:
		with open("test.txt", "w", encoding="utf-8") as file:
			file.write(str(message.attachments))
		tools.log_tools.logging(log_file=tools.config.path_log, string = f"[bot][info]Пользователь {user_name} действие <Прикрепил фото или видео>", time=datetime.datetime.now(), limit=10)
		attach = []
		if message.attachments[0].photo:
			for i in range(len(message.attachments)):
				print(message.attachments[i].photo.sizes[-5].url)
				urllib.request.urlretrieve(message.attachments[i].photo.sizes[-5].url, f"photo{i}.png")
				attach.append(f"photo{i}.png")

			ctx.set("content", attach)
			customers.add(message.from_id, attach)
			
		# elif message.attachments[0].video:
		# 	for i in range(len(message.attachments)):
		# 		attach.append(f"video{i}.mp4")
		# 		urllib.request.urlretrieve(message.attachments[i].video.url, f"video{i}.mp4")
	else:
		tools.log_tools.logging(log_file=tools.config.path_log, string = f"[bot][info]Пользователь {user_name} действие <Не прикрепил фото или видео>", time=datetime.datetime.now(), limit=10)
		ctx.set("content", None)
		customers.add(message.from_id, None)
		
	await bot.state_dispenser.set(message.peer_id, PostCreator.PUBLISH_DATE)
	return await message.answer("Напишите время поста в формате гггг-мм-дд чч:мм")



@bot.on.private_message(state=PostCreator.PUBLISH_DATE)
async def create_post(message: Message):
	users_info = await bot.api.users.get(message.from_id)
	user_name = users_info[0].first_name + " " + users_info[0].last_name

	if tools.post_date.valid_date(publish_date=message.text) == -1:
		tools.log_tools.logging(log_file=tools.config.path_log, string = f"[bot][error]Пользователь {user_name} действие <Не верно ввел дату>", time=datetime.datetime.now(), limit=10)
		await bot.state_dispenser.set(message.peer_id, PostCreator.PUBLISH_DATE)
		return await message.answer("ошибка ввода даты, пожалуйста введите дату заного в формате гггг-мм-дд чч:мм")
		

	elif tools.post_date.valid_date(publish_date=message.text) == 0:
		tools.log_tools.logging(log_file=tools.config.path_log, string = f"[bot][error]Пользователь {user_name} действие <Ввел дату меньше текущей>", time=datetime.datetime.now(), limit=10)
		await bot.state_dispenser.set(message.peer_id, PostCreator.PUBLISH_DATE)
		return await message.answer("Введенная дата не может быть меньше текущей, пожалуйста введите дату заного в формате гггг-мм-дд чч:мм")


	elif tools.post_date.valid_date(publish_date=message.text) == 1:
		tools.log_tools.logging(log_file=tools.config.path_log, string = f"[bot][info]Пользователь {user_name} действие <Верно ввел дату>", time=datetime.datetime.now(), limit=10)
		if tools.post_date.date_is_free(date_to_check=message.text+":00") == 1:
			tools.log_tools.logging(log_file=tools.config.path_log, string = f"[bot][info]Пользователь {user_name} действие <Ввел свободную дату>", time=datetime.datetime.now(), limit=10)
			ctx.set("publish_date", message.text+":00")
			customers.add(message.from_id, message.text+":00")

			keyboard = Keyboard(inline=True)
			keyboard.add(Text("Отсутствует"))
			await bot.state_dispenser.set(message.peer_id, PostCreator.REFERENCE)
			return await message.answer("Пожалуйста укажите источник вашего поста", keyboard=keyboard)
		elif tools.post_date.date_is_free(date_to_check=message.text+":00") == 0:
			tools.log_tools.logging(log_file=tools.config.path_log, string = f"[bot][error]Пользователь {user_name} действие <Ввел занятую дату>", time=datetime.datetime.now(), limit=10)
			await bot.state_dispenser.set(message.peer_id, PostCreator.PUBLISH_DATE)
			return await message.answer("Введенная дата занята, пожалуйста введите другую дату с интервалом в 3 часа или больше")
		elif tools.post_date.date_is_free(date_to_check=message.text+":00") == -1:
			tools.log_tools.logging(log_file=tools.config.path_log, string = f"[bot][error]Пользователь {user_name} действие <Ввел занятый день>", time=datetime.datetime.now(), limit=10)
			await bot.state_dispenser.set(message.peer_id, PostCreator.PUBLISH_DATE)
			return await message.answer("На данный день закончились записи, попробуйте ввести другой день")



@bot.on.private_message(state=PostCreator.REFERENCE)
async def create_post(message: Message):
	users_info = await bot.api.users.get(message.from_id)
	user_name = users_info[0].first_name + " " + users_info[0].last_name

	if message.text == "Отсутствует":
		tools.log_tools.logging(log_file=tools.config.path_log, string = f"[bot][info]Пользователь {user_name} действие <Не ввел ссылку на источник>", time=datetime.datetime.now(), limit=10)
		ctx.set("reference", None)
		customers.add(message.from_id, None)

		keyboard = Keyboard(inline=True)
		keyboard.add(Text("Да"))
		keyboard.row()
		keyboard.add(Text("Нет"))
		await bot.state_dispenser.set(message.peer_id, PostCreator.CLOSE_COMMENTS)
		return await message.answer("Хотите ли вы закрыть комментарии в вашем посте?", keyboard=keyboard)
	else:
		tools.log_tools.logging(log_file=tools.config.path_log, string = f"[bot][info]Пользователь {user_name} действие <Ввел ссылку на источник>", time=datetime.datetime.now(), limit=10)
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
	users_info = await bot.api.users.get(message.from_id)
	user_name = users_info[0].first_name + " " + users_info[0].last_name

	if message.text == "Да":
		tools.log_tools.logging(log_file=tools.config.path_log, string = f"[bot][info]Пользователь {user_name} действие <Закрыл коментарии>", time=datetime.datetime.now(), limit=10)
		ctx.set("close_comments", True)
		customers.add(message.from_id, True)
		keyboard = Keyboard(inline=True)
		keyboard.add(Text("Да"))
		keyboard.row()
		keyboard.add(Text("Нет"))

		await bot.state_dispenser.set(message.peer_id, PostCreator.CONFIRM)
		return await message.answer("Убедитесь что все данные введены правильно, иначе отменить действие не получится. Если готовы продолжить нажмите Да, иначе Нет", keyboard=keyboard)

	
	elif message.text == "Нет":
		tools.log_tools.logging(log_file=tools.config.path_log, string = f"[bot][info]Пользователь {user_name} действие <Не закрыл коментарии>", time=datetime.datetime.now(), limit=10)
		ctx.set("close_comments", False)
		customers.add(message.from_id, False)
		keyboard = Keyboard(inline=True)
		keyboard.add(Text("Да"))
		keyboard.row()
		keyboard.add(Text("Нет"))

		await bot.state_dispenser.set(message.peer_id, PostCreator.CONFIRM)
		return await message.answer("Убедитесь что все данные введены правильно, иначе отменить действие не получится. Если готовы продолжить нажмите Да, иначе Нет", keyboard=keyboard)

	else:
		tools.log_tools.logging(log_file=tools.config.path_log, string = f"[bot][error]Пользователь {user_name} действие <Не верно выбрал ответ>", time=datetime.datetime.now(), limit=10)
		await message.answer("Не корректный ввод!")
		await bot.state_dispenser.set(message.peer_id, PostCreator.CLOSE_COMMENTS)
		return await message.answer("Хотите ли вы закрыть комментарии в вашем посте?", keyboard=keyboard)


@bot.on.private_message(state=PostCreator.CONFIRM)
async def create_post(message: Message):
	users_info = await bot.api.users.get(message.from_id)
	user_name = users_info[0].first_name + " " + users_info[0].last_name

	if message.text == "Да":
		tools.log_tools.logging(log_file=tools.config.path_log, string = f"[bot][info]Пользователь {user_name} действие <Закончил создание поста>", time=datetime.datetime.now(), limit=10)
		await message.answer("Создание поста, пожалуйста подождите...")

		if tools.wall.post(
			message        = customers.get(message.from_id)[2],
			attachments    = customers.get(message.from_id)[3],
			publish_date   = datetime.datetime.strptime(customers.get(message.from_id)[4], "%Y-%m-%d %H:%M:%S"),
			close_comments = customers.get(message.from_id)[6],
			copyright      = customers.get(message.from_id)[5],
			customer	   = message.from_id,
			):
			await message.answer("Успешное создание поста, он будет опубликован вовремя!")
			
			if customers.get(message.from_id)[3] != None:
				for item in customers.get(message.from_id)[3]:
					os.remove(item)
			
			count = db.read_one_query(f"SELECT count_posts FROM customers WHERE user_id={int(message.from_id)};")
			count = int(''.join(map(str, count)))
			if count is None: count = 0
			db.write_query(f"INSERT OR REPLACE INTO customers (user_id, latest_post, count_posts) VALUES ({message.from_id}, \"{str(customers.get(message.from_id)[4])}\", {count+1})")
			
			customers.set(user_id=message.from_id, param=["WAIT"])
		else:
			await message.answer("При создании поста возникла ошибка на стороне сервера! Не волнуйтесь ваш оплаченый пост не исчез! Обратитесь в поддержку или повторите попытку позже")

	
	elif message.text == "Нет":
		tools.log_tools.logging(log_file=tools.config.path_log, string = f"[bot][info]Пользователь {user_name} действие <Отменил создание поста>", time=datetime.datetime.now(), limit=10)
		keyboard = Keyboard(inline=True)
		keyboard.add(Text("Создать рекламный пост"))
		await message.answer("Давайте приступим к созданию поста для этого нажмите кнопку ниже", keyboard=keyboard)

	else:
		tools.log_tools.logging(log_file=tools.config.path_log, string = f"[bot][info]Пользователь {user_name} действие <Не верно выбрал ответ>", time=datetime.datetime.now(), limit=10)
		keyboard = Keyboard(inline=True)
		keyboard.add(Text("Создать рекламный пост"))
		await message.answer("Я тебя не понял", keyboard=keyboard)



if __name__ == "__main__":
	bot.run_forever()