from picamera2 import Picamera2
import time

picam2 = Picamera2()

# Настройка кропа (x, y, width, height) относительно полного разрешения
crop_width, crop_height = 1000, 800  # Желаемые размеры после кропа
crop_x, crop_y = 200, 150  # Смещение от левого верхнего угла

# Создаем конфигурацию с кропом
config = picam2.create_still_configuration(
    main={
        "size": (crop_width, crop_height),  # Размер выхода
        "format": "RGB888",
    },
    raw={
        "size": picam2.sensor_resolution,  # Полное разрешение сенсора
    },
    buffer_count=2,
    controls={
        "ScalerCrop": (crop_x, crop_y, crop_width, crop_height),  # Область кропа
    }
)

picam2.configure(config)
preview_config = picam2.create_preview_configuration()
picam2.start(show_preview=True)
time.sleep(20)
# Захватываем кадр (уже обрезанный)
image = picam2.capture_array("main")  # shape=(crop_height, crop_width, 3)
picam2.stop()