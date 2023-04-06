import os
import shutil
import datetime

def create_log(log_file: str) -> bool:
	with open(file=log_file, mode='w', encoding="utf-8") as file:
		pass

def logging(log_file: str, string: str, time: str, limit: int) -> bool:
	if os.path.exists(log_file):
		check_limit(log_file=log_file, limit=limit)
		try:
			with open(file=log_file, mode='a', encoding="utf-8") as file:
				file.write(f"[{time}]{string}\n")
			return True
		except Exception:
			return False
	else:
		create_log(log_file)
		logging(log_file=log_file, string=string, time=time, limit=limit)

def check_limit(log_file: str, limit: int):

	if ((os.path.getsize(log_file)) / 1000) > limit:
		FILE_LIMIT = f"{datetime.datetime.now().year}-{datetime.datetime.now().month}-{datetime.datetime.now().day}_old_log.txt"

		with open(FILE_LIMIT, mode='w', encoding="utf-8") as file:
			pass

		shutil.copyfile(os.path.abspath(log_file), os.path.abspath(FILE_LIMIT))

		with open(log_file, mode="w", encoding="utf-8") as file:
			pass
