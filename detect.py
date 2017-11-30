import time
import face_logging
import face_recognition
from picamera import PiCamera

camera = PiCamera()
# might have to change this based on how the picamera is oriented 
camera.rotation = 180
# default is 50
camera.brightness = 60
camera.resolution = (320, 240)

picture_of_me = face_recognition.load_image_file("me.jpg")
my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]

next_photo = 0
INTERVAL = 15
count = 0

while 1:
    if time.time() < next_photo:
        time.sleep(0.1)
        continue

    next_photo = time.time() + INTERVAL
    print()
    print("taking a photo...")
    camera.start_preview()
    time.sleep(2)
    camera.capture('image.jpg')
    camera.stop_preview()
    print("looking for faces...")
    unknown_picture = face_recognition.load_image_file("image.jpg")
    face_locations = face_recognition.face_locations(unknown_picture)

    if len(face_locations) <= 0:
        print("no faces found...")
        continue

    print("I found " + str(len(face_locations)) + " face(s)")
    print("is it me?")
    unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]
    results = face_recognition.compare_faces([my_face_encoding], unknown_face_encoding)
    count += 1
    if results[0] == True:
        print("It is!")
        face_logging.log_add("Allen")
        if count % 20 == 0: # save a photo log every 20*15 = 300 seconds, or 5 minutes
            face_logging.photo_add("Allen")
    else:
        print("Nope")
        face_logging.log_add("Unknown")
        face_logging.photo_add("Unknown") # save a photo log of every unknown face
    
    






