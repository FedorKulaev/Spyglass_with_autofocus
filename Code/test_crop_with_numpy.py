from picamera2 import Picamera2, Preview
import numpy as np
import time

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
    """Альтернативный расчет FoM без OpenCV"""
    # Конвертация в grayscale (формула NTSC)
    gray = image_roi[:,:,0] * 0.299 + image_roi[:,:,1] * 0.587 + image_roi[:,:,2] * 0.114
    
    # Расчет градиентов через numpy
    grad_x = np.abs(np.gradient(gray, axis=1))
    grad_y = np.abs(np.gradient(gray, axis=0))
    
    # FoM как сумма абсолютных значений градиентов
    return np.sum(grad_x + grad_y)

picam2.set_controls({"LensPosition": 8})
try:
    for i in range(1000):
        # Захват кадра
        image = picam2.capture_array("main")
        # Выделение ROI
        roi = image[roi_y:roi_y+roi_height, roi_x:roi_x+roi_width]
        # Расчет и вывод FoM
        fom = calculate_fom(roi)
        print(f"FoM: {fom:.2f}")
    
        # Задержка для контроля частоты обновления
        time.sleep(0.5)  # 10 FPS
        

except KeyboardInterrupt:
    pass

finally:
    picam2.stop()
