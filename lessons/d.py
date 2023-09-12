import shutil

source_folder = "lesson-6"  # Папка, которую нужно скопировать

for i in range(7, 37):  # Создаем копии с номерами от 7 до 36
    destination_folder = f"lesson-{i}"  # Имя новой папки
    shutil.copytree(source_folder, destination_folder)