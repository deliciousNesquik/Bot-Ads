import tool.json_tools
import tool.log_tools
import datetime
import tool.wall
import time

while True:
	array = tool.json_tools.find_overdue_post_json("tool/posts.json", indent=4)

	if len(array) > 0:
		tool.log_tools.logging(log_file="tool/log.txt", string = f"[check post]Все найденные в файле просроченные посты: {array}", time=datetime.datetime.now(), limit=10)

		for date in array:
			tool.log_tools.logging(log_file="tool/log.txt", string = f"[check post]Дата поста: {date}", time=datetime.datetime.now(), limit=10)
			ids = tool.wall._get_overdue_post(date)
			if ids != None:
				tool.log_tools.logging(log_file="tool/log.txt", string = f"[check post]Его id на стене вк: {ids}", time=datetime.datetime.now(), limit=10)
				tool.wall.delete(post_id=ids)
				tool.log_tools.logging(log_file="tool/log.txt", string = "[check post]Данный пост удалён\n\n", time=datetime.datetime.now(), limit=10)
			else:
				tool.log_tools.logging(log_file="tool/log.txt", string = f"[check post]id поста не найден", time=datetime.datetime.now(), limit=10)
			time.sleep(4)

	else:
		tool.log_tools.logging(log_file="tool/log.txt", string = "[check post]Просроченные посты в файле не найдены!\n\n", time=datetime.datetime.now(), limit=10)

	time.sleep(10)