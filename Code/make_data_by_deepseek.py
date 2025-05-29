import pigpio
import time
from picamera2 import Picamera2
import numpy as np
import matplotlib.pyplot as plt
from threading import Thread

# Настройки оборудования
GPIO_CONFIG = {
    "AIN1": 17,
    "AIN2": 27,
    "PWMA": 18,
    "STBY": 22,
    "CONC": 4
}

# Параметры системы
ROI_SIZE = (40, 40)  # Уменьшенная область интереса
ROI_POS = (910, 520)
MOTOR_SPEED = 70
SAMPLE_DELAY = 0.001  # 1 ms между измерениями

# Инициализация GPIO
pi = pigpio.pi()
for pin in [GPIO_CONFIG["AIN1"], GPIO_CONFIG["AIN2"], GPIO_CONFIG["PWMA"], GPIO_CONFIG["STBY"]]:
    pi.set_mode(pin, pigpio.OUTPUT)
pi.set_mode(GPIO_CONFIG["CONC"], pigpio.INPUT)
pi.set_pull_up_down(GPIO_CONFIG["CONC"], pigpio.PUD_DOWN)
pi.write(GPIO_CONFIG["STBY"], 1)

# Настройка ШИМ
pi.set_PWM_frequency(GPIO_CONFIG["PWMA"], 1000)
pi.set_PWM_range(GPIO_CONFIG["PWMA"], 255)

# Инициализация камеры с оптимизированными настройками
picam2 = Picamera2()
config = picam2.create_preview_configuration(
    main={"size": (ROI_SIZE[0]*2, ROI_SIZE[1]*2), "format": "RGB888"},
    controls={"AfMode": 0, "LensPosition": 10, "FrameRate": 60}
)
picam2.configure(config)
picam2.start()

# Глобальные переменные для многопоточности
data_queue = []
running = True
roi_slice = (slice(ROI_POS[1], ROI_POS[1]+ROI_SIZE[1]), 
             slice(ROI_POS[0], ROI_POS[0]+ROI_SIZE[0]))

def motor_control(speed, direction):
    """Оптимизированное управление мотором"""
    pi.write(GPIO_CONFIG["AIN1"], direction > 0)
    pi.write(GPIO_CONFIG["AIN2"], direction < 0)
    pi.set_PWM_dutycycle(GPIO_CONFIG["PWMA"], speed if direction else 0)

def calculate_fom(image):
    """Быстрый расчет показателя резкости по красному каналу"""
    return np.sum(np.abs(np.gradient(image[..., 0])))

def capture_thread():
    """Поток для непрерывного захвата данных"""
    global data_queue
    while running:
        try:
            image = picam2.capture_array("main")[roi_slice]
            data_queue.append(calculate_fom(image))
            time.sleep(SAMPLE_DELAY)
        except:
            break

def main():
    global running
    Thread(target=capture_thread, daemon=True).start()
    
    try:
        while pi.read(GPIO_CONFIG["CONC"]):
            # Цикл движения мотора
            motor_control(MOTOR_SPEED, 1)
            start_time = time.monotonic()
            
            # Сбор данных в течение 50 ms
            while time.monotonic() - start_time < 0.05:
                pass
                
            # Остановка и сбор оставшихся данных
            motor_control(0, 0)
            time.sleep(0.02)  # Краткая пауза
            array.extend(data_queue)
            data_queue.clear()
            
    finally:
        running = False
        motor_control(0, 0)
        pi.write(GPIO_CONFIG["STBY"], 0)
        pi.stop()
        picam2.stop()
        
        # Анализ и визуализация
        plt.figure(figsize=(12, 6))
        plt.plot(array, 'b-', linewidth=0.5)
        plt.title(f"Профиль резкости ({len(array)} измерений)")
        plt.grid(True)
        plt.show()
        
        print(f"Собрано точек: {len(array)}")
        print(f"Максимальное значение: {np.max(array)}")
        print(f"Средняя частота: {len(array)/(time.monotonic()-start_time):.1f} Hz")

if __name__ == "__main__":
    main()