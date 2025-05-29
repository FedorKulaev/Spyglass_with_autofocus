from picamera2 import Picamera2, Preview
from time import sleep

camera = Picamera2()
preview_config = camera.create_preview_configuration()
camera.configure(preview_config)
camera.start(show_preview=True)
camera.set_controls({"AfMode": 0})
for i in range(7, 13):
    camera.set_controls({"LensPosition": i})
    print(i)
    sleep(2)