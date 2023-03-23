import tool.wall
import datetime

date_time = datetime.datetime(
	year=datetime.datetime.now().year,
	month=datetime.datetime.now().month,
	day=datetime.datetime.now().day,
	hour=22,
	minute=6,
	seconds=0,
	)

print(tool.wall.post(message = "hello1", publish_date=date_time, close_comments = 0, from_group = 1))