import os
from PIL import Image

def get_image_size(image_path):
    with Image.open(image_path) as img:
        return img.size  # Возвращает (ширина, высота)


def parse_annotations(folder_path, image_folder_path):
    counts_1 = 0  # Количество 1 (каски)
    counts_0 = 0  # Количество 0 (без каски)
    total_area_1 = 0  # Сумма площадей объектов с лейблом 1
    areas_1 = []  # Список для хранения площадей объектов с лейблом 1
    max_area_1 = 0  # Максимальная площадь объекта с лейблом 1
    max_area_image_path = None  # Путь к изображению с максимальной площадью
    max_area_helmet_size = None  # Размер каски с максимальной площадью (width, height)
    min_area_1 = float('inf')  # Минимальная площадь объекта с лейблом 1
    min_area_image_path = None  # Путь к изображению с минимальной площадью
    min_area_helmet_size = None  # Размер каски с минимальной площадью (width, height)
    min_area_ratio = float('inf')  # Минимальное соотношение площади каски к площади изображения
    max_area_ratio = 0  # Максимальное соотношение площади каски к площади изображения

    for file_name in os.listdir(folder_path):
        if file_name.endswith('.txt'):
            # Получаем путь к изображению, предполагается, что имя файла .txt совпадает с именем изображения
            image_path = os.path.join(image_folder_path,
                                      file_name.replace('.txt', '.jpg'))  # или .png, в зависимости от формата

            # Получаем размеры изображения
            image_width, image_height = get_image_size(image_path)
            image_area = image_width * image_height  # Площадь изображения

            with open(os.path.join(folder_path, file_name), 'r') as file:
                lines = file.readlines()
                for line in lines:
                    data = line.strip().split()
                    label = int(data[0])  # 1 или 0 (наличие каски)
                    x_center, y_center, width, height = map(float, data[1:])

                    # Нормализация ширины и высоты для каждого изображения
                    width *= image_width
                    height *= image_height

                    # Округляем размеры до целых пикселей (минимум 1 пиксель)
                    width = max(1, round(width))
                    height = max(1, round(height))

                    # Если каска есть, добавляем её площадь
                    if label == 1:
                        counts_1 += 1
                        area = width * height
                        total_area_1 += area
                        areas_1.append(area)

                        # Вычисляем соотношение площади каски к площади изображения
                        area_ratio = (area / image_area) * 100  # В процентах

                        # Обновляем минимальное и максимальное соотношение
                        if area_ratio < min_area_ratio:
                            min_area_ratio = area_ratio
                        if area_ratio > max_area_ratio:
                            max_area_ratio = area_ratio

                        # Обновляем максимальную площадь, путь к изображению и размер каски
                        if area > max_area_1:
                            max_area_1 = area
                            max_area_image_path = image_path
                            max_area_helmet_size = (width, height)  # Сохраняем размер каски

                        # Обновляем минимальную площадь, путь к изображению и размер каски
                        if area < min_area_1:
                            min_area_1 = area
                            min_area_image_path = image_path
                            min_area_helmet_size = (width, height)  # Сохраняем размер каски

                    if label == 0:
                        counts_0 += 1

    # Вычисляем среднюю площадь для объектов с лейблом 1
    avg_area_1 = total_area_1 / counts_1 if counts_1 > 0 else 0

    return counts_1, counts_0, avg_area_1, areas_1, min_area_1, min_area_image_path, min_area_helmet_size, max_area_1, max_area_image_path, max_area_helmet_size, min_area_ratio, max_area_ratio


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
    max_area_1_total = 0  # Максимальная площадь для всего датасета
    max_area_image_path_total = None  # Путь к изображению с максимальной площадью для всего датасета
    max_area_helmet_size_total = None  # Размер каски с максимальной площадью для всего датасета
    min_area_1_total = float('inf')  # Минимальная площадь для всего датасета
    min_area_image_path_total = None  # Путь к изображению с минимальной площадью для всего датасета
    min_area_helmet_size_total = None  # Размер каски с минимальной площадью для всего датасета
    min_area_ratio_total = float('inf')  # Минимальное соотношение площади каски к площади изображения для всего датасета
    max_area_ratio_total = 0  # Максимальное соотношение площади каски к площади изображения для всего датасета

    # Проходим по всем папкам
    for folder_name, folder_path in folders.items():
        image_folder_path = image_folders[folder_name]

        # Получаем статистику по каждой папке
        counts_1, counts_0, avg_area_1, areas_1, min_area_1, min_area_image_path, min_area_helmet_size, max_area_1, max_area_image_path, max_area_helmet_size, min_area_ratio, max_area_ratio = parse_annotations(folder_path, image_folder_path)

        # Добавляем в суммарные счетчики
        total_counts_1 += counts_1
        total_counts_0 += counts_0
        total_area_1 += sum(areas_1)
        total_areas_1.extend(areas_1)

        # Обновляем минимальное и максимальное соотношение для всего датасета
        if min_area_ratio < min_area_ratio_total:
            min_area_ratio_total = min_area_ratio
        if max_area_ratio > max_area_ratio_total:
            max_area_ratio_total = max_area_ratio

        # Обновляем максимальную площадь, путь к изображению и размер каски для всего датасета
        if max_area_1 > max_area_1_total:
            max_area_1_total = max_area_1
            max_area_image_path_total = max_area_image_path
            max_area_helmet_size_total = max_area_helmet_size

        # Обновляем минимальную площадь, путь к изображению и размер каски для всего датасета
        if min_area_1 < min_area_1_total:
            min_area_1_total = min_area_1
            min_area_image_path_total = min_area_image_path
            min_area_helmet_size_total = min_area_helmet_size

        # Выводим результаты по каждой папке
        print(f"Folder: {folder_name}")
        print(f"  Counts of 1 (helmets): {counts_1}")
        print(f"  Counts of 0 (no helmet): {counts_0}")
        print(f"  Average area of 1 (helmets): {avg_area_1:.0f}"'px')
        print(f"  Minimum area of 1 (helmets): {min_area_1:.0f}"'px')
        print(f"  Image with minimum area: {min_area_image_path}")
        print(f"  Size of smallest helmet: {min_area_helmet_size[0]}x{min_area_helmet_size[1]}")
        print(f"  Maximum area of 1 (helmets): {max_area_1:.0f}"'px')
        print(f"  Image with maximum area: {max_area_image_path}")
        print(f"  Size of largest helmet: {max_area_helmet_size[0]}x{max_area_helmet_size[1]}")
        print(f"  Minimum area ratio (helmet to image): {min_area_ratio:.10f}%")
        print(f"  Maximum area ratio (helmet to image): {max_area_ratio:.2f}%")
        print(f"  Percentage of 1: {(counts_1 / (counts_1 + counts_0)) * 100:.2f}%")
        print(f"  Percentage of 0: {(counts_0 / (counts_1 + counts_0)) * 100:.2f}%")
        print()

    # Вычисляем среднюю площадь для всего датасета
    avg_area_1_total = total_area_1 / total_counts_1 if total_counts_1 > 0 else 0

    # Выводим суммарные результаты
    print(f"Total counts of 1 (helmets): {total_counts_1}")
    print(f"Total counts of 0 (no helmet): {total_counts_0}")
    print(f"Total average area of 1 (helmets): {avg_area_1_total:.0f}"'px')
    print(f"Total minimum area of 1 (helmets): {min_area_1_total:.0f}"'px')
    print(f"Image with minimum area: {min_area_image_path_total}")
    print(f"Size of smallest helmet: {min_area_helmet_size_total[0]}x{min_area_helmet_size_total[1]}")
    print(f"Total maximum area of 1 (helmets): {max_area_1_total:.0f}"'px')
    print(f"Image with maximum area: {max_area_image_path_total}")
    print(f"Size of largest helmet: {max_area_helmet_size_total[0]}x{max_area_helmet_size_total[1]}")
    print(f"Total minimum area ratio (helmet to image): {min_area_ratio_total:.10f}%")
    print(f"Total maximum area ratio (helmet to image): {max_area_ratio_total:.2f}%")
    print(f"Total percentage of 1: {(total_counts_1 / (total_counts_1 + total_counts_0)) * 100:.2f}%")
    print(f"Total percentage of 0: {(total_counts_0 / (total_counts_1 + total_counts_0)) * 100:.2f}%")


process_dataset('combined_dataset/images')