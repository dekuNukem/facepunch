# facepunch: A facial recognition punch clock on Raspberry Pi

I made it to track how many hours I spend in my office. The idea is rather simple: the picamera takes a photo every 15 seconds, and if my face is found in the photo, my presence is logged. This is then added up to calculate my exact working hours every week. The result is displayed on an OLED screen.