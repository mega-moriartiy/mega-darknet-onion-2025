import os
import shutil

def main():
    print("🧹 Умная чистка рабочего стола")
    print("—" * 50)

    # Определяем путь к рабочему столу
    desktop = os.path.join(os.path.expanduser("~"), "Рабочий стол")
    
    # Для англоязычных систем (если папка называется "Desktop")
    if not os.path.exists(desktop):
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    
    if not os.path.exists(desktop):
        print("❌ Не удалось найти рабочий стол. Проверь системные настройки.")
        return

    # Папки для сортировки
    folders = {
        "Документы": [".txt", ".doc", ".docx", ".odt"],
        "Изображения": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"],
        "PDF": [".pdf"],
        "Музыка": [".mp3", ".wav", ".flac", ".ogg"],
        "Видео": [".mp4", ".avi", ".mkv", ".mov"],
        "Архивы": [".zip", ".rar", ".7z", ".tar", ".gz"]
    }

    # Создаём папки, если их нет
    created = 0
    for folder in folders:
        path = os.path.join(desktop, folder)
        if not os.path.exists(path):
            os.mkdir(path)
            print(f"📁 Создана папка: {folder}")
            created += 1

    if created > 0:
        print("—" * 50)

    # Сканируем рабочий стол
    moved = 0
    for filename in os.listdir(desktop):
        filepath = os.path.join(desktop, filename)

        # Пропускаем папки и скрытые файлы
        if os.path.isdir(filepath) or filename.startswith('.'):
            continue

        # Получаем расширение
        _, ext = os.path.splitext(filename)
        ext = ext.lower()

        # Ищем, в какую папку переместить
        moved_file = False
        for folder, extensions in folders.items():
            if ext in extensions:
                dest_folder = os.path.join(desktop, folder)
                dest_path = os.path.join(dest_folder, filename)

                # Если файл с таким именем уже есть — добавим номер
                counter = 1
                original_dest = dest_path
                while os.path.exists(dest_path):
                    name, ext_part = os.path.splitext(filename)
                    dest_path = os.path.join(dest_folder, f"{name}_{counter}{ext_part}")
                    counter += 1

                shutil.move(filepath, dest_path)
                print(f"✅ {filename} → {folder}/")
                moved += 1
                moved_file = True
                break

        # Если расширение не найдено — в "Разное"
        if not moved_file:
            other_folder = os.path.join(desktop, "Разное")
            if not os.path.exists(other_folder):
                os.mkdir(other_folder)
            shutil.move(filepath, os.path.join(other_folder, filename))
            print(f"📁 {filename} → Разное/")
            moved += 1

    print("—" * 50)
    if moved > 0:
        print(f"🎉 Чистка завершена! Перемещено файлов: {moved}")
    else:
        print("🧹 На рабочем столе не было файлов для сортировки.")

    print("Теперь у тебя порядок! 💫")

if __name__ == "__main__":
    main()
