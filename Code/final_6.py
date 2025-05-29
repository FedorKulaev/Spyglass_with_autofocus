import pigpio
import time
from picamera2 import Picamera2, Preview
import numpy as np

# Пины GPIO
AIN1 = 17   # IN1 (направление)
AIN2 = 27   # IN2 (направление)
PWMA = 18   # PWM (скорость)
STBY = 22   # STBY (включение драйвера)
conc = 4
button = 10      #Прописать номер пина

pi = pigpio.pi()

# Настройка пинов
pi.set_mode(AIN1, pigpio.OUTPUT)
pi.set_mode(AIN2, pigpio.OUTPUT)
pi.set_mode(STBY, pigpio.OUTPUT)
pi.set_mode(PWMA, pigpio.OUTPUT)
pi.set_mode(conc, pigpio.INPUT)
pi.set_pull_up_down(conc, pigpio.PUD_DOWN)
pi.set_mode(button, pigpio.INPUT)
pi.set_pull_up_down(button, pigpio.PUD_DOWN)
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
    controls={"AfMode": 0, "LensPosition": 10}  # Ручной режим фокуса
)
picam2.configure(config)
picam2.start()

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
    time.sleep(0.03)
    motor_control(70, 0)
    time.sleep(0.02)
    return rez()

def turn_off():
    pi.write(AIN1, 0)
    pi.write(AIN2, 0)
  # Подобрал наиболее близкое к глазу



def pusk():
    # Двигаем в начало отсчёта
    arr = []
    if not pi.read(conc):  #Если замкнут
        cash = next_step(-1)
        cash = next_step(-1)
        if pi.read(conc): 
            motor_control(120, -1)
            while pi.read(conc):
                time.sleep(0.01)
            else:
                motor_control(70, 0)
    else:
        motor_control(120, -1)
        while pi.read(conc):
            time.sleep(0.01)
        else:
            motor_control(70, 0)
            
    arr.append(next_step(1))
    arr.append(next_step(1))
    arr.append(next_step(1))
    while pi.read(conc):
        arr.append(next_step(1))

    m = max(arr)
    for i in range(1, len(arr)+1):
        if (arr[-i] == m):
            break
        cash = next_step(-1)
    turn_off()

turn_off()
while True:
    time.sleep(0.05)
    if pi.read(button):
        pusk()
        time.sleep(1.4)

turn_off()
pi.write(STBY, 0)
pi.stop()
picam2.stop()






