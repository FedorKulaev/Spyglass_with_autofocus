import pigpio
import time

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

# Пример работы:
try:
    motor_control(70, 1)
    time.sleep(0.5)
    pi.write(AIN1, 0)
    pi.write(AIN2, 0)
finally:
    pi.write(AIN1, 0)
    pi.write(AIN2, 0)
    pi.write(STBY, 0)  # Выключить драйвер
    pi.stop()
