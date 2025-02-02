import os
import shutil

# Пути к первому датасету
dataset1_test_images = r"C:\\Users\\Admin\\PycharmProjects\\helmet_detection_project\\df1\test\\images"
dataset1_test_labels = r"C:\\Users\\Admin\\PycharmProjects\\helmet_detection_project\\df1\\test\\labels"
dataset1_train_images = r"C:\\Users\\Admin\\PycharmProjects\\helmet_detection_project\\df1\\train\\images"
dataset1_train_labels = r"C:\\Users\\Admin\\PycharmProjects\\helmet_detection_project\\df1\\train\\labels"
dataset1_val_images = r"C:\\Users\\Admin\\PycharmProjects\\helmet_detection_project\\df1\\valid\\images"
dataset1_val_labels = r"C:\\Users\\Admin\\PycharmProjects\\helmet_detection_project\\df1\\valid\\labels"

# Пути ко второму датасету
dataset2_test_images = r"C:\\Users\\Admin\\PycharmProjects\\helmet_detection_project\\df3\\test\\images"
dataset2_test_labels = r"C:\\Users\\Admin\\PycharmProjects\\helmet_detection_project\\df3\\test\\labels"
dataset2_train_images = r"C:\\Users\\Admin\\PycharmProjects\\helmet_detection_project\\df3\\train\\images"
dataset2_train_labels = r"C:\\Users\\Admin\\PycharmProjects\\helmet_detection_project\\df3\\train\\labels"
dataset2_val_images = r"C:\\Users\\Admin\\PycharmProjects\\helmet_detection_project\\df3\\valid\\images"
dataset2_val_labels = r"C:\\Users\\Admin\\PycharmProjects\\helmet_detection_project\\df3\\valid\\labels"

# Папка для объединенного датасета
output_dataset = r"C:\\Users\\Admin\\PycharmProjects\\helmet_detection_project\\combined_dataset"
output_images = os.path.join(output_dataset, "images")
output_labels = os.path.join(output_dataset, "labels")

# Создаем папки для объединенного датасета
os.makedirs(output_images, exist_ok=True)
os.makedirs(output_labels, exist_ok=True)


# Функция обработки одного набора данных
def process_dataset(images_path, labels_path, split, output_images, output_labels, filter_classes):
    image_dir = images_path
    label_dir = labels_path

    output_image_dir = os.path.join(output_images, split)
    output_label_dir = os.path.join(output_labels, split)

    os.makedirs(output_image_dir, exist_ok=True)
    os.makedirs(output_label_dir, exist_ok=True)

    for label_file in os.listdir(label_dir):
        label_path = os.path.join(label_dir, label_file)
        image_path = os.path.join(image_dir, label_file.replace('.txt', '.jpg'))

        # Проверяем, существует ли файл изображения
        if not os.path.exists(image_path):
            print(f"Изображение {image_path} не найдено. Пропускаем.")
            continue

        try:
            # Читаем аннотации
            with open(label_path, 'r') as f:
                lines = f.readlines()

            filtered_lines = []
            for line in lines:
                class_id, *coords = line.strip().split()
                class_id = int(class_id)
                if class_id in filter_classes:  # Сохраняем только нужные классы
                    filtered_lines.append(f"{class_id} {' '.join(coords)}")

            if filtered_lines:
                # Копируем изображение
                shutil.copy(image_path, os.path.join(output_image_dir, os.path.basename(image_path)))

                # Записываем фильтрованные аннотации
                with open(os.path.join(output_label_dir, label_file), 'w') as f:
                    f.writelines('\n'.join(filtered_lines))

                print(f"Файл {label_file} успешно обработан.")
        except Exception as e:
            print(f"Ошибка при обработке {label_file}: {e}")


# Обработка первого датасета (классы 0 и 1)
process_dataset(dataset1_train_images, dataset1_train_labels, 'train', output_images, output_labels,
                filter_classes=[0, 1])
process_dataset(dataset1_val_images, dataset1_val_labels, 'val', output_images, output_labels, filter_classes=[0, 1])
process_dataset(dataset1_test_images, dataset1_test_labels, 'test', output_images, output_labels, filter_classes=[0, 1])

# Обработка второго датасета (классы helmet и no-helmet)
process_dataset(dataset2_train_images, dataset2_train_labels, 'train', output_images, output_labels,
                filter_classes=[0, 1])
process_dataset(dataset2_val_images, dataset2_val_labels, 'val', output_images, output_labels, filter_classes=[0, 1])
process_dataset(dataset2_test_images, dataset2_test_labels, 'test', output_images, output_labels, filter_classes=[0, 1])