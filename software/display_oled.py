import time
import random
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106
from PIL import ImageDraw
from PIL import ImageFont
from datetime import datetime, timezone, timedelta
import RPi.GPIO as GPIO

reset_pin = 17

def oled_reset():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(reset_pin, GPIO.OUT, initial=GPIO.LOW)
    GPIO.output(reset_pin, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(reset_pin, GPIO.HIGH)
    time.sleep(0.1)

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

oled_reset()

serial = i2c(port=1, address=0x3d) # sometimes the address is 0x3c for some reason
device = sh1106(serial)
font = ImageFont.truetype('cc.ttf', 28)
oox = 0 # OLED burn-in prevention variables
ooy = 0
shift_amount = 2

while 1:
    time.sleep(10)
    with canvas(device) as draw:
        try:
            today_sum, week_sum, last_face = get_sum()
        except Exception as e:
            print(e)
            continue
        # put a border around the screen if a face recognition was successful in the last 2 minutes
        if last_face < 60 * 2:
            draw.rectangle(device.bounding_box, outline="white", fill="black")
        # otherwise don't draw the border
        elif last_face < 60 * 15:
            draw.rectangle(device.bounding_box, outline="black", fill="black")
        # if no face for more than 15 minutes, turn off the OLED
        else:
            device.clear()
            continue
        oox = random.randint(-shift_amount, shift_amount) # randomly shift the displayed item around 
        ooy = random.randint(-shift_amount, shift_amount) # slightly to prevent OLED burn-in
        print(str(oox) + ", " + str(ooy))
        draw.text((7 + oox, 3 + ooy), "Today", font=font, fill="white")
        draw.text((7 + oox, 32 + ooy), "Week", font=font, fill="white")
        draw.text((80 + oox, 3 + ooy), make_hhmm(today_sum), font=font, fill="white")
        draw.text((80 + oox, 32 + ooy), make_hhmm(week_sum), font=font, fill="white")
