import os
from datetime import datetime

def get_ts_str():
	return datetime.utcnow().replace(microsecond=0).isoformat(sep='T') + "Z"

def get_ts_filename():
	return get_ts_str().replace(":", '_')

def log_add(whose_face):
	with open("punch_log.txt", "a+") as f:
		f.write(get_ts_str() + " " + str(whose_face) + " \n")

def photo_add(facename):
	os.system("cp ./image.jpg ./photo_log/" + get_ts_filename() + "_" + facename + ".jpg")
