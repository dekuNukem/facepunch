# facepunch: A facial recognition punch clock on Raspberry Pi

facepunch is a facial recognition punch clock that keeps track of how many hours you spend in front of your desk.

![Alt text](resources/front.jpg)

The concept is rather simple: the picamera takes a photo every 15 seconds, the time is recorded if my face is found in the photo. This is then added up to calculate my exact working hours every week. The result is displayed on an OLED screen.