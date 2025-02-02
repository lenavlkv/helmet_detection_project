import os
import numpy as np

def parse_annotations(folder_path):
    counts_1 = 0  # Количество 1 (каски)
    counts_0 = 0  # Количество 0 (без каски)


    for file_name in os.listdir(folder_path):

        if file_name.endswith('.txt'):

            with open(os.path.join(folder_path, file_name), 'r') as file:
                lines = file.readlines()
                for line in lines:
                    data = line.strip().split()
                    label = int(data[0])  # 1 или 0 (наличие каски)
                    x_center, y_center, width, height = map(float, data[1:])

                    # Если каска есть, добавляем её размер в helmet_sizes
                    if label == 1:
                        counts_1 += 1

                    if label == 0:
                        counts_0 += 1

    return counts_1, counts_0


# Функция для обработки всех папок
def process_dataset():
    # Папки с аннотациями
    folders = {
        'train': 'combined_dataset/labels/train',
        'test': 'combined_dataset/labels/test',
        'valid': 'combined_dataset/labels/val'
    }

    # Суммарные счетчики для всех папок
    total_counts_1 = 0
    total_counts_0 = 0

    # Проходим по всем папкам
    for folder_name, folder_path in folders.items():
        # Получаем статистику по каждой папке
        counts_1, counts_0 = parse_annotations(folder_path)

        # Добавляем в суммарные счетчики
        total_counts_1 += counts_1
        total_counts_0 += counts_0

        # Выводим результаты по каждой папке
        print(f"Folder: {folder_name}")
        print(f"  Counts of 1 (helmets): {counts_1}")
        print(f"  Counts of 0 (no helmet): {counts_0}")
        print(f"  Percentage of 1: {(counts_1 / (counts_1 + counts_0)) * 100:.2f}%")
        print(f"  Percentage of 0: {(counts_0 / (counts_1 + counts_0)) * 100:.2f}%")
        print()


    # Вычисляем процентное соотношение для суммарных данных
    total_percentage_1 = (total_counts_1 / (total_counts_1 + total_counts_0)) * 100
    total_percentage_0 = (total_counts_0 / (total_counts_1 + total_counts_0)) * 100

    # Выводим суммарные результаты
    print(f"Total counts of 1 (helmets): {total_counts_1}")
    print(f"Total counts of 0 (no helmet): {total_counts_0}")
    print(f"Total percentage of 1: {total_percentage_1:.2f}%")
    print(f"Total percentage of 0: {total_percentage_0:.2f}%")


process_dataset()