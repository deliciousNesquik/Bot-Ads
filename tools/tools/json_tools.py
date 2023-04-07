from datetime import datetime

from . import log_tools
import json
import os

# filename:			str      - переменная для хранения пути к файлу с постами
# dictionary:		dict     - словарь для добавления или перезаписи данных в файле
# indent:			int      - переменная для хранения отступа в файле json
# id_post:			str 	 - переменная для хранения псевдо id поста в файле json

def create_json(filename: str) -> bool:
	with open(filename, mode='w', encoding="utf-8") as file:
		file.write("{}")

def read_json(filename: str) -> dict:
	if os.path.exists(filename):
		with open(filename, encoding="utf-8") as file:
			return json.loads(file.read())
	else:
		create_json(filename=filename)
		read_json(filename=filename)

def write_json(filename: str, dictionary: dict, indent: int) -> bool:
	with open(filename, 'w', encoding="utf-8") as file:
		file.write(json.dumps(dictionary, indent=indent))

def append_json(filename: str, dictionary: dict, indent: int) -> bool:
	data = read_json(filename=filename)
	data.update(dictionary)
	write_json(filename=filename, dictionary=data, indent=indent)

def delete_json(filename: str, id_post: str, indent: int) -> bool:
	data = read_json(filename=filename)
	del data[id_post]
	write_json(filename=filename, dictionary=data, indent=indent)

def find_overdue_post_json(filename: str, indent: int) -> list:
	data = read_json(filename)
	date_post_to_delete = []
	id_post_to_delete = []

	#проход по постам
	for key, value in data.items():

		#запоминаем id поста
		id_post = key
		log_tools.logging(log_file=config.path_log, string = f"[json_tools]Обработка поста №{id_post}", time=datetime.now(), limit=10)

		#прохожимся по элементам поста и ищем параметр со врменем поста
		for key, value in value.items():

			#если нашли параметр
			if key == "publish_date":

				#дата которая на посте
				date_post = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
				log_tools.logging(log_file=config.path_log, string = f"[json_tools]дата этого поста:{date_post}", time=datetime.now(), limit=10)
				#актуальная дата
				date_now = datetime.strptime(f"{datetime.now().year}-{datetime.now().month}-{datetime.now().day} {datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}", "%Y-%m-%d %H:%M:%S")

				log_tools.logging(log_file=config.path_log, string = f"[json_tools]сегодняшняя дата:{date_now}", time=datetime.now(), limit=10)
				#если со времени публикации поста прошло три дня
				if date_now > date_post:
					log_tools.logging(log_file=config.path_log, string = f"[json_tools]дата данного поста больше чем сегодняшняя дата", time=datetime.now(), limit=10)
					log_tools.logging(log_file=config.path_log, string = f"[json_tools]разница во времени: {abs(date_post - date_now).total_seconds()}\n\n", time=datetime.now(), limit=10)
					#if abs(date_post - date_now).total_seconds() >= 3 * 24 * 60 * 60:
					if abs(date_post - date_now).total_seconds() >= 60:
						#заносим в список id поста для того чтобы потом его удалить
						date_post_to_delete.append(date_post)
						id_post_to_delete.append(id_post)
				else:
					log_tools.logging(log_file=config.path_log, string = f"[json_tools]данный пост пока что не является просроченным\n\n", time=datetime.now(), limit=10)


	for ids in id_post_to_delete:
		delete_json(filename=filename, id_post=ids, indent=indent)

def find_date_post_json(filename: str, indent: int) -> list:
	data = read_json(filename)

	date_post = []
	for key, value in data.items():
		for key, value in value.items():
			if key == "publish_date":
				date_post.append(value)

	return date_post