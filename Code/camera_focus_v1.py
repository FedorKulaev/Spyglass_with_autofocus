# Подключаем необходимые библиотеки
from picamera2 import Picamera2, Preview
from time import sleep
from libcamera import controls
from pprint import pprint
 
 
def is_focused_waiting(cam_object):
    success = cam_object.autofocus_cycle()
    return success
    
    
def is_focused_async(cam_object):
    job = cam_object.autofocus_cycle(wait=False)
    success = cam_object.wait(job)
    return success    
    
# Создаём объект для работы с камерой
camera = Picamera2()  
# Настраиваем окно предпросмотра
preview_config = camera.create_preview_configuration()
camera.configure(preview_config)
 
# Запускаем окно предпросмотра сигнала с камеры на экране поверх всех окон
#camera.start_preview(Preview.QTGL)
 
# Включаем камеру
camera.start(show_preview=True)
#camera.set_controls({"AfMode": controls.AfModeEnum.Continuous})

focus = 5.0

for i in range(1, 10000):
    b = int(input())
    
    if (b == 3):
        focus += 0.1
    elif b == 1:
        focus -= 0.1
    elif b == 6:
        focus += 0.3
    elif b == 4:
        focus -= 0.3
    camera.set_controls({"LensPosition": focus})	
    #print("cycle", i, "; is_camera_focused: ", is_focused_async(camera), sep='')
    sleep(0.5)
    metadata = camera.capture_metadata()
    #print(metadata["FocusFoM"])# Проверяем, есть ли полезные данные (например, FocusFoM)
    print(metadata["LensPosition"], metadata["FocusFoM"])
