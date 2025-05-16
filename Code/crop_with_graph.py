from picamera2 import Picamera2
import numpy as np
import time
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

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

def calculate_fom(image_roi):
    """Альтернативный расчет FoM без OpenCV"""
    # Конвертация в grayscale (формула NTSC)
    gray = image_roi[:,:,0] * 0.299 + image_roi[:,:,1] * 0.587 + image_roi[:,:,2] * 0.114
    
    # Расчет градиентов через numpy
    grad_x = np.abs(np.gradient(gray, axis=1))
    grad_y = np.abs(np.gradient(gray, axis=0))
    
    # FoM как сумма абсолютных значений градиентов
    return np.sum(grad_x + grad_y)

# Настройка отображения
plt.ion()  # Включаем интерактивный режим
fig, ax = plt.subplots(1, figsize=(10, 6))
ax.set_title("Camera Preview with ROI")

try:
    for i in range(15):
        picam2.set_controls({"LensPosition": 8})
        print(i)
        for j in range(10):
            # Захват кадра
            image = picam2.capture_array("main")
            
            # Выделение ROI
            roi = image[roi_y:roi_y+roi_height, roi_x:roi_x+roi_width]
            
            # Расчет FoM
            fom = calculate_fom(roi)
            
            # Очистка предыдущего изображения
            ax.clear()
            
            # Отображение текущего кадра
            ax.imshow(image)
            
            # Добавление прямоугольника ROI
            roi_rect = Rectangle((roi_x, roi_y), roi_width, roi_height,
                               linewidth=2, edgecolor='r', facecolor='none')
            ax.add_patch(roi_rect)
            
            # Вывод значения FoM
            ax.text(roi_x, roi_y - 10, f"FoM: {fom:.2f}", 
                   color='red', fontsize=12, bbox=dict(facecolor='white', alpha=0.7))
            
            # Обновление графика
            plt.pause(0.01)

        
except KeyboardInterrupt:
    print("Stopping...")

finally:
    picam2.stop()
    plt.ioff()
    plt.close()