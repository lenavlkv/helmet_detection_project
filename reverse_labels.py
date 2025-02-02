import os

# Папки для обработки
input_folders = ['test', 'train', 'valid']
output_folder = 'df3'

# Функция для изменения первой цифры в строке
def modify_line(line):
    # Разбиваем строку на элементы
    parts = line.split()

    # Заменяем первую цифру
    if parts[0] == '0':
        parts[0] = '1'
    elif parts[0] == '1':
        parts[0] = '0'

    # Возвращаем строку с измененной первой цифрой
    return ' '.join(parts) + '\n'

# Создаем структуру папок в df3
for folder in input_folders:
    for subfolder in ['images', 'labels']:
        # Полный путь для папки в df1 и df3
        input_path = os.path.join('df1', folder, subfolder)
        output_path = os.path.join(output_folder, folder, subfolder)

        # Если такой папки нет в df3, создаем ее
        os.makedirs(output_path, exist_ok=True)

        # Проходим по всем файлам в labels папке
        for filename in os.listdir(input_path):

            if filename.endswith('.txt'):
                input_file_path = os.path.join(input_path, filename)
                output_file_path = os.path.join(output_path, filename)

                with open(input_file_path, 'r') as infile:
                    lines = infile.readlines()

                # Модифицируем строки
                modified_lines = [modify_line(line) for line in lines]

                # Сохраняем измененные данные в новый файл
                with open(output_file_path, 'w') as outfile:
                    outfile.writelines(modified_lines)

print("Обработка завершена!")