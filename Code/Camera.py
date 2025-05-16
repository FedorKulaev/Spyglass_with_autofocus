from picamera2 import Picamera2, Preview
from time import sleep

camera = Picamera2()
preview_config = camera.create_preview_configuration()
camera.configure(preview_config)
camera.start(show_preview=True)
for i in range(12, 18):
    camera.set_controls({"LensPosition": i/2})
    print(i)
    sleep(1)