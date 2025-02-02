import os
import numpy as np
from PIL import Image

def get_image_size(image_path):
    with Image.open(image_path) as img:
        return img.size  # Возвращает (ширина, высота)


def parse_annotations(folder_path, image_folder_path):
    counts_1 = 0  # Количество 1 (каски)
    counts_0 = 0  # Количество 0 (без каски)
    total_area_1 = 0  # Сумма площадей объектов с лейблом 1
    areas_1 = []  # Список для хранения площадей объектов с лейблом 1

    for file_name in os.listdir(folder_path):
        if file_name.endswith('.txt'):
            # Получаем путь к изображению, предполагается, что имя файла .txt совпадает с именем изображения
            image_path = os.path.join(image_folder_path,
                                      file_name.replace('.txt', '.jpg'))  # или .png, в зависимости от формата

            # Получаем размеры изображения
            image_width, image_height = get_image_size(image_path)

            with open(os.path.join(folder_path, file_name), 'r') as file:
                lines = file.readlines()
                for line in lines:
                    data = line.strip().split()
                    label = int(data[0])  # 1 или 0 (наличие каски)
                    x_center, y_center, width, height = map(float, data[1:])

                    # Нормализация ширины и высоты для каждого изображения
                    width *= image_width
                    height *= image_height

                    # Если каска есть, добавляем её площадь
                    if label == 1:
                        counts_1 += 1
                        area = width * height
                        total_area_1 += area
                        areas_1.append(area)

                    if label == 0:
                        counts_0 += 1

    # Вычисляем среднюю площадь для объектов с лейблом 1
    avg_area_1 = total_area_1 / counts_1 if counts_1 > 0 else 0

    return counts_1, counts_0, avg_area_1, areas_1


# Функция для обработки всех папок
def process_dataset(image_folder_base_path):
    # Папки с аннотациями
    folders = {
        'train': 'combined_dataset/labels/train',
        'test': 'combined_dataset/labels/test',
        'valid': 'combined_dataset/labels/val'
    }

    # Папки с изображениями
    image_folders = {
        'train': 'combined_dataset/images/train',
        'test': 'combined_dataset/images/test',
        'valid': 'combined_dataset/images/val'
    }

    # Суммарные счетчики для всех папок
    total_counts_1 = 0
    total_counts_0 = 0
    total_area_1 = 0  # Сумма всех площадей объектов с лейблом 1
    total_areas_1 = []  # Список для хранения всех площадей объектов с лейблом 1

    # Проходим по всем папкам
    for folder_name, folder_path in folders.items():
        image_folder_path = image_folders[folder_name]

        # Получаем статистику по каждой папке
        counts_1, counts_0, avg_area_1, areas_1 = parse_annotations(folder_path, image_folder_path)

        # Добавляем в суммарные счетчики
        total_counts_1 += counts_1
        total_counts_0 += counts_0
        total_area_1 += sum(areas_1)
        total_areas_1.extend(areas_1)

        # Выводим результаты по каждой папке
        print(f"Folder: {folder_name}")
        print(f"  Counts of 1 (helmets): {counts_1}")
        print(f"  Counts of 0 (no helmet): {counts_0}")
        print(f"  Average area of 1 (helmets): {avg_area_1:.0f}"'px')
        print(f"  Percentage of 1: {(counts_1 / (counts_1 + counts_0)) * 100:.2f}%")
        print(f"  Percentage of 0: {(counts_0 / (counts_1 + counts_0)) * 100:.2f}%")
        print()

    # Вычисляем среднюю площадь для всего датасета
    avg_area_1_total = total_area_1 / total_counts_1 if total_counts_1 > 0 else 0

    # Выводим суммарные результаты
    print(f"Total counts of 1 (helmets): {total_counts_1}")
    print(f"Total counts of 0 (no helmet): {total_counts_0}")
    print(f"Total average area of 1 (helmets): {avg_area_1_total:.0f}"'px')
    print(f"Total percentage of 1: {(total_counts_1 / (total_counts_1 + total_counts_0)) * 100:.2f}%")
    print(f"Total percentage of 0: {(total_counts_0 / (total_counts_1 + total_counts_0)) * 100:.2f}%")


process_dataset('combined_dataset/images')