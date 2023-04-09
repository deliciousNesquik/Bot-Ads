from vk_api import VkUpload
from vk_api import VkTools
from vk_api import VkApi

from . import json_tools
from . import log_tools
from . import config
from . import upload
from . import login
from . import tool
import datetime


# login:			str      - переменная для хранения логина от аккаунта вконтакте
# password:		    str      - переменная для хранения пароля от аккаунта вконтакте
# owner_id: 		int      - id группы
# from_group: 	    bool     - 0(от группы) 1(от пользователя)
# message: 		    str      - сообщение
# attachments: 	    str      - прикрепления
# close_comments:   bool     - 0(открытые комментарии) 1(закрытые комментарии)
# publish_date: 	str      - дата публикации в формате (2023, 2, 19, 18, 50, 00)
# copyright: 		str      - ссылка на источник

# session:          VkApi    - объект вк api
# uploader:		    VkUpload - объект вк api для загрузки фото
# tools:			VkTools  - объект вк api в нашем случае для получения полной стены вк
# unix_time:		Datetime - переменная для хранения времени в unix формате


def post(publish_date:datetime, message:str = None, attachments:list = None, close_comments:int = 0, copyright:str = None, from_group:int = 0) -> bool:
	log_tools.logging(log_file=config.path_log, string = f"[wall.post][info]Создание поста в вк...", time=datetime.datetime.now(), limit=10)

	global session, uploader

	if message == None and attachments == None:
		log_tools.logging(log_file=config.path_log, string = f"[wall.post][error]При создании поста не указаны аргументы сообщения и прикреплений!", time=datetime.datetime.now(), limit=10)
		return "При публикации поста нужно чтобы хотя бы один параметр был не пустым"

	if attachments is not None:
		if attachments[0].split(".")[-1] in config.photo_expansion:
			log_tools.logging(log_file=config.path_log, string = f"[wall.post][info]Обнаружены фото, загрузка...", time=datetime.datetime.now(), limit=10)
			attachments = uploader.upload_photo(images=attachments)
			log_tools.logging(log_file=config.path_log, string = f"[wall.post][info]Успешная загрузка фото", time=datetime.datetime.now(), limit=10)

		elif attachments[0].split(".")[-1] in config.video_expansion:
			log_tools.logging(log_file=config.path_log, string = f"[wall.post][info]Обнаружены видео, загрузка...", time=datetime.datetime.now(), limit=10)
			attachments = uploader.upload_video(videos=attachments)
			log_tools.logging(log_file=config.path_log, string = f"[wall.post][info]Успешная загрузка видео", time=datetime.datetime.now(), limit=10)

	date_time = datetime.datetime(year=datetime.datetime.now().year, month=datetime.datetime.now().month, day=datetime.datetime.now().day, hour=datetime.datetime.now().hour, minute=datetime.datetime.now().minute)
	if date_time > publish_date:
		log_tools.logging(log_file=config.path_log, string = f"[wall.post][error]Дата поста меньше чем текущая", time=datetime.datetime.now(), limit=10)
		return "Время публикации поста должна быть больше чем время в данный момент"

	try:
		id_post = session.wall.post(
			owner_id       = -config.owner_id,
			from_group     = from_group,
			message        = message,
			attachments    = attachments,
			publish_date   = _unix_time(publish_date),
			close_comments = close_comments,
			copyright      = copyright,
			)
		log_tools.logging(log_file=config.path_log, string = f"[wall.post][info]Успешное создание поста\n\n", time=datetime.datetime.now(), limit=10)
		
		json_tools.append_json(
		filename = config.path_json, 
		dictionary = {
				str(id_post['post_id']): {
					'owner_id'       : -config.owner_id,
					'from_group'     : from_group,
					'message'        : message,
					'attachments'    : attachments,
					'publish_date'	 : str(publish_date),
					'close_comments' : close_comments,
					'copyright'      : copyright,
				}
			},
		indent = 4,
		)
		return True
	except Exception as ex:
		log_tools.logging(log_file=config.path_log, string = f"[wall.post][error]Ошибка создания поста {ex}\n\n", time=datetime.datetime.now(), limit=10)
		return False

def delete(post_id:int) -> bool:
	global session
	log_tools.logging(log_file=config.path_log, string = f"[wall.delete][info]Удаление поста в вк...", time=datetime.datetime.now(), limit=10)
	try:
		delete = session.wall.delete(
			owner_id = -config.owner_id,
			post_id  = post_id,
			)
		log_tools.logging(log_file=config.path_log, string = f"[wall.delete][info]Удаление поста в вк прошло успешно", time=datetime.datetime.now(), limit=10)
	except Exception as ex:
		log_tools.logging(log_file=config.path_log, string = f"[wall.delete][error]Ошибка удаления поста {ex}", time=datetime.datetime.now(), limit=10)

def _get_overdue_post(publish_date: datetime) -> int:
	publish_date = _unix_time(publish_date)
	wall         = _get_full_wall()

	for key in wall:
		if key['date'] == publish_date:
			return key['id']

def _get_full_wall() -> dict:
	global tools
	wall = tools.get_all(
		'wall.get', 100, 
		{
			'owner_id': -config.owner_id
		}
	)
	return wall['items']

def _unix_time(date_time: datetime) -> int:
	return int(date_time.timestamp())

global session, uploader, tools
session  = login.Authorization(config.token_wall).get_api()
uploader = upload.Uploaders(session)
tools    = tool.Tools(session).get_tools()