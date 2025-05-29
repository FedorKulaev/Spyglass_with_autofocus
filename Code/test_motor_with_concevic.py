import pigpio
import time

# Пины GPIO
AIN1 = 17   # IN1 (направление)
AIN2 = 27   # IN2 (направление)
PWMA = 18   # PWM (скорость)
STBY = 22   # STBY (включение драйвера)
conc = 4


pi = pigpio.pi()

# Настройка пинов
pi.set_mode(AIN1, pigpio.OUTPUT)
pi.set_mode(AIN2, pigpio.OUTPUT)
pi.set_mode(STBY, pigpio.OUTPUT)
pi.set_mode(PWMA, pigpio.OUTPUT)

pi.set_mode(conc, pigpio.INPUT)
pi.set_pull_up_down(conc, pigpio.PUD_DOWN)

# Включить драйвер
pi.write(STBY, 1)

def motor_control(speed, direction):
    if direction == 1:
        pi.write(AIN1, 1)
        pi.write(AIN2, 0)
    elif direction == -1:
        pi.write(AIN1, 0)
        pi.write(AIN2, 1)
    pi.set_PWM_dutycycle(PWMA, speed)  # speed: 0-255

# print("est tok") if conc_in else print("net sveta")
try:
    motor_control(80, 1)
    for i in range(1000):
        if pi.read(conc) == 0:
            pi.write(AIN1, 0)
            pi.write(AIN2, 0)
            pi.write(STBY, 0)
            break
        time.sleep(0.01)
finally:
    pi.write(AIN1, 0)
    pi.write(AIN2, 0)
    pi.write(STBY, 0)
    pi.stop()


