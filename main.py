import os
import re
import base64
import argparse
from pathlib import Path

def image_to_base64(image_path):
    """Конвертирует изображение в строку base64."""
    img_extension = Path(image_path).suffix.lower().replace('.', '')
    if img_extension == 'jpeg':
        img_extension = 'jpg'
        
    with open(image_path, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode('utf-8')
        return f"data:image/{img_extension};base64,{encoded_string}"

def process_directory(target_dir):
    dir_path = Path(target_dir)
    if not dir_path.is_dir():
        return

    md_files = list(dir_path.glob("*.md"))
    if not md_files:
        return
    
    md_file_path = md_files[0]
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.webp')
    images = sorted([f for f in dir_path.iterdir() if f.suffix.lower() in image_extensions])
    
    if not images:
        return

    footnotes = []
    processed_images = []

    # Добавляем разделитель для футера, если его еще нет
    if "\n---" not in content:
        content += "\n\n---"

    for idx, img_path in enumerate(images, start=1):
        img_name = img_path.name
        img_base64 = image_to_base64(img_path)
        
        # Создаем уникальный идентификатор для сноски
        footnote_id = f"fig_{idx}"
        footnote_marker = f"[^{footnote_id}]"
        footnote_content = f"[^{footnote_id}]: ![]({img_base64})"

        # Ищем упоминание файла в тексте (в любом виде)
        # 1. Пытаемся заменить стандартный синтаксис ![alt](path)
        pattern = re.compile(rf'!\[(.*?)\]\({re.escape(img_name)}\)')
        
        if pattern.search(content):
            content = pattern.sub(footnote_marker, content)
            footnotes.append(footnote_content)
            processed_images.append(img_path)
        elif img_name in content:
            # 2. Если просто имя файла текстом
            content = content.replace(img_name, footnote_marker)
            footnotes.append(footnote_content)
            processed_images.append(img_path)

    # Записываем сноски в самый конец файла
    if footnotes:
        content += "\n\n" + "\n\n".join(footnotes) + "\n"

    with open(md_file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    # Удаляем оригиналы
    for img_path in processed_images:
        os.remove(img_path)
        print(f"[{target_dir}] Зашито в футер и удалено: {img_path.name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dirs", nargs='+')
    args = parser.parse_args()

    for d in args.dirs:
        process_directory(d)
