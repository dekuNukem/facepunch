# facepunch: A facial recognition punch clock on Raspberry Pi

facepunch is a facial recognition punch clock that keeps track of how many hours you spend in front of your desk.

![Alt text](resources/front.jpg)

The concept is rather simple: the picamera takes a photo every 15 seconds, the time is recorded if my face is found in the photo. This is then added up to calculate my exact working hours every week. The result is displayed on an OLED screen.

## Get it working

### Set up Raspberry pi

[Install the latest Raspbian here](https://www.raspberrypi.org/documentation/installation/installing-images/)

### Wire up OLED display and camera

[OLED install guide](https://learn.adafruit.com/ssd1306-oled-displays-with-raspberry-pi-and-beaglebone-black/wiring)

[Camera install guide](https://projects.raspberrypi.org/en/projects/getting-started-with-picamera)

I put the two together on a perf board that plug into the header.

### Install required libraries

[luma OLED library](https://luma-oled.readthedocs.io/en/latest/install.html)

[face_recognition library](https://gist.github.com/ageitgey/1ac8dbe8572f3f533df6269dab35df65)

There is a typo in the above instruction, at the step `Download and install dlib v19.6:`

change 

`sudo python3 setup.py install --compiler-flags "-mpfu=neon"` 

to

`sudo python3 setup.py install --compiler-flags "-mfpu=neon"`

Note how the `-mfpu` flag was misspelled.

### Provide your photo

The program needs a picture of your face in order to learn what you look like. Get a picture of your well-lit face in a clean background and name it `me.jpg` and place it in the software folder. The resolution should be around 400x400 otherwise the processing time is going to be long. An example is already provided so just replace it with your own.

### Run the program

Run `python3 detect.py` to start face detection and logging.

Run `python3 display_oled.py` to display time statistics on the OLED.

Or if you don't have an OLED, run `python3 display_text.py` to print the statistics to the terminal.

You might have to play with `camera.rotation` and `camera.brightness` at the beginning of `detect.py` depending on how your camera is oriented and your lighting condition. You can open up `image.jpg` to see the latest photo taken.

