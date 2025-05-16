import pigpio
import time
from picamera2 import Picamera2, Preview
import numpy as np

# Пины GPIO
AIN1 = 17   # IN1 (направление)
AIN2 = 27   # IN2 (направление)
PWMA = 18   # PWM (скорость)
STBY = 22   # STBY (включение драйвера)
pi = pigpio.pi()

# Настройка пинов
pi.set_mode(AIN1, pigpio.OUTPUT)
pi.set_mode(AIN2, pigpio.OUTPUT)
pi.set_mode(STBY, pigpio.OUTPUT)
pi.set_mode(PWMA, pigpio.OUTPUT)

# Включить драйвер
pi.write(STBY, 1)


def motor_control(speed, direction):
    if direction == 1:
        pi.write(AIN1, 1)
        pi.write(AIN2, 0)
    elif direction == -1:
        pi.write(AIN1, 0)
        pi.write(AIN2, 1)
    elif direction == 0:
        pi.write(AIN1, 0)
        pi.write(AIN2, 0)
    pi.set_PWM_dutycycle(PWMA, speed)  # speed: 0-255
    

# Инициализация камеры
picam2 = Picamera2()

# Параметры области анализа (ROI)
roi_width, roi_height = 150, 150
roi_x, roi_y = 910, 520

# Конфигурация камеры
config = picam2.create_preview_configuration(
    main={"size": (1920, 1080), "format": "RGB888"},
    controls={"AfMode": 0, "LensPosition": 0.0}  # Ручной режим фокуса
)
picam2.configure(config)
picam2.start()
picam2.set_controls({"LensPosition": 0})
def calculate_fom(image_roi):
    # Конвертация в grayscale (формула NTSC)
    gray = image_roi[:,:,0] * 0.299 + image_roi[:,:,1] * 0.587 + image_roi[:,:,2] * 0.114
    
    # Расчет градиентов через numpy
    grad_x = np.abs(np.gradient(gray, axis=1))
    grad_y = np.abs(np.gradient(gray, axis=0))
    
    # FoM как сумма абсолютных значений градиентов
    return np.sum(grad_x + grad_y)


# Функция для вывода значения резкости
def rez():
    image = picam2.capture_array("main")
    roi = image[roi_y:roi_y+roi_height, roi_x:roi_x+roi_width]
    return calculate_fom(roi)

# Функция немного двигает линзу в направлении d и выводит новое значение резкости
def next_step(d):
    motor_control(70, d)
    time.sleep(0.05)
    return rez()

picam2.set_controls({"LensPosition": 8})  # Подобрал наиболее близкое к глазу

d = 1
current = rez()
print(current)
try:
    for i in range(25):
        next_count = next_step(d)
        print(d, next_count)
        if current > next_count:
            d = -d
        current = next_step(d)
        
finally:
    pi.write(AIN1, 0)
    pi.write(AIN2, 0)
    pi.write(STBY, 0)  # Выключить драйвер
    pi.stop()
    picam2.stop()
