from . import json_tools
import datetime

def valid_date(publish_date: str) -> int:
	date_now = datetime.datetime.strptime(f"{datetime.datetime.now().year}-{datetime.datetime.now().month}-{datetime.datetime.now().day} {datetime.datetime.now().hour}:{datetime.datetime.now().minute}:{datetime.datetime.now().second}", "%Y-%m-%d %H:%M:%S")
	try:
		date_post = datetime.datetime.strptime(publish_date, "%Y-%m-%d %H:%M:%S")
		if date_post < date_now:
			return 0
		else:
			return 1
	except Exception:
		return -1



def get_date_post(filename: str) -> list:
	date = json_tools.read_json(filename)
	date_posts = []

	for key, value in data.items():
		for key, value in value.items():
			if key == "publish_date":
				date_posts.append(value)

	return date_posts



def get_count_post_day(filename: str) -> bool
	pass


def free_date(filename: str, publish_date: str, date_posts: list) -> bool:
	for date in date_posts:
		if abs((publish_date - date).total_seconds()) < 3 * 60 * 60:
			return False




if __name__ == "__main__":
	publish_date = datetime.datetime(year=2023, month=3, day=23, hour=15, minute=0, seconds=0)
	free_date(publish_date=publish_date)