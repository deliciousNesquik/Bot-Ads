from . import json_tools
from . import config
from datetime import datetime

def valid_date(publish_date: str) -> int:
	date_now = datetime.strptime(f"{datetime.now().year}-{datetime.now().month}-{datetime.now().day} {datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}", "%Y-%m-%d %H:%M:%S")
	try:
		date_post = datetime.strptime(publish_date+":0", "%Y-%m-%d %H:%M:%S")
		if date_post < date_now:
			return 0
		else:
			return 1
	except Exception:
		return -1

def _day_is_free(date_to_check: datetime, dates: list) -> bool:
	count = 0

	for date in dates:
		date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
		if date.day == date_to_check.day:
			count += 1

	return True if count < 3 else False

def _time_is_free(date_to_check: datetime, dates: list) -> bool:
	is_free = True

	for date in dates:
		date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
		if date.day == date_to_check.day:
			if abs(date - date_to_check).total_seconds() < 3 * 60 * 60:
				return False
		elif date.day != date_to_check.day:
			break

	return is_free

def date_is_free(date_to_check: datetime) -> bool:
	date_to_check = datetime.strptime(date_to_check, "%Y-%m-%d %H:%M:%S")
	dates = json_tools.find_date_post_json(filename=config.path_json, indent=4)

	if _day_is_free(date_to_check, dates):
		if _time_is_free(date_to_check, dates):
			return 1
		else:
			return 0

	else:
		return -1