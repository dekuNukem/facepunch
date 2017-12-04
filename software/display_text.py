import time
import random
from datetime import datetime, timezone, timedelta

def parse_ts(ts_str):
    return datetime.strptime(ts_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)

def get_sum():
    beginning_today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0).replace(tzinfo=timezone.utc)
    beginning_this_week = (beginning_today - timedelta(days=datetime.today().weekday())).replace(tzinfo=timezone.utc)
    today_sum = 0
    week_sum = 0
    with open("punch_log.txt") as log_file:
        prev_ts = parse_ts(log_file.readline().split(" ")[0])
        for line in log_file:
            if "Allen" not in line:
                continue
            this_ts = parse_ts(line.split(" ")[0])
            diff_sec = int((this_ts - prev_ts).total_seconds())

            if this_ts > beginning_today and diff_sec <= 60 * 5:
                today_sum += diff_sec
            if this_ts > beginning_this_week and diff_sec <= 60 * 5:
                week_sum += diff_sec
            prev_ts = this_ts

    last_face_ts = (datetime.today().replace(tzinfo=timezone.utc) - prev_ts).total_seconds()
    return today_sum, week_sum, last_face_ts

def sec_to_hr_min(sec):
    return int(sec / 3600), int((sec % 3600) / 60)

def make_hhmm(sec):
    hours, minutes = sec_to_hr_min(sec)
    return str(hours) + ":" + str(minutes).zfill(2)

while 1:
    try:
        today_sum, week_sum, last_face = get_sum()
    except Exception as e:
        print(e)
        time.sleep(5)
        continue
    print("today: " + make_hhmm(today_sum))
    print("this week: " + make_hhmm(week_sum))
    print()
    time.sleep(10)