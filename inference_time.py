import torch
from PIL import Image
import time
import os
import ultralytics
from ultralytics import YOLO
# Загрузка модели (предположим, что модель уже обучена и сохранена в файл 'best.pt')
#model = torch.hub.load('yolov8s.pt', 'custom', path='C://Users//Admin//PycharmProjects//helmet_detection_project//runs//detect//train5//weights//best.pt')

model_path = 'C://Users//Admin//PycharmProjects//helmet_detection_project//runs//detect//train7//weights//best.pt'
model = YOLO(model_path)


# Выбор устройства (GPU или CPU)
device = 'cpu'
model.to(device)

# Загрузка тестового изображения
test_images_path = 'C://Users//Admin//PycharmProjects//helmet_detection_project//combined_dataset//images//test'
image_files = [os.path.join(test_images_path, f) for f in os.listdir(test_images_path) if f.endswith('.jpg')]

total_time = 0
num_images = len(image_files)

for img_path in image_files:
    img = Image.open(img_path)
    start_time = time.time()
    results = model(img)
    end_time = time.time()
    total_time += (end_time - start_time)

average_inference_time = total_time / num_images
average_fps = 1 / average_inference_time

print(f"Среднее время инференса: {average_inference_time:.4f} секунд")
print(f"Средний FPS: {average_fps:.2f}")