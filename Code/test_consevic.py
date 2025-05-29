import pigpio
import time

# Пины GPIO
AIN1 = 17   # IN1 (направление)
AIN2 = 27   # IN2 (направление)
PWMA = 18   # PWM (скорость)
STBY = 22   # STBY (включение драйвера)
conc_in = 4


pi = pigpio.pi()

# Настройка пинов
pi.set_mode(AIN1, pigpio.OUTPUT)
pi.set_mode(AIN2, pigpio.OUTPUT)
pi.set_mode(STBY, pigpio.OUTPUT)
pi.set_mode(PWMA, pigpio.OUTPUT)

pi.set_mode(conc_in, pigpio.INPUT)
pi.set_pull_up_down(conc_in, pigpio.PUD_DOWN)

# Включить драйвер
pi.write(STBY, 1)


# print("est tok") if conc_in else print("net sveta")
try:
    
    while True:
        print(pi.read(conc_in))
        time.sleep(0.05)
finally:
      # Выключить драйвер
    pi.stop()

