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
    # Сортируем для предсказуемого порядка (img_ref_0, img_ref_1...)
    images = sorted([f for f in dir_path.iterdir() if f.suffix.lower() in image_extensions])
    
    if not images:
        return

    references = []
    processed_images = []

    for idx, img_path in enumerate(images):
        img_name = img_path.name
        img_base64 = image_to_base64(img_path)
        
        ref_id = f"img_ref_{idx}"
        ref_marker = f"![][{ref_id}]"
        ref_definition = f"[{ref_id}]: {img_base64}"

        # 1. Замена стандартного синтаксиса ![alt](filename)
        pattern = re.compile(rf'!\[.*?\]\({re.escape(img_name)}\)')
        
        if pattern.search(content):
            content = pattern.sub(ref_marker, content)
            references.append(ref_definition)
            processed_images.append(img_path)
        elif img_name in content:
            # 2. Если имя файла просто упомянуто текстом (например, в вашем дампе)
            content = content.replace(img_name, ref_marker)
            references.append(ref_definition)
            processed_images.append(img_path)

    # Добавляем список определений в конец файла
    if references:
        # Проверяем, есть ли уже пустые строки в конце
        content = content.rstrip() 
        content += "\n\n" + "\n".join(references) + "\n"

    with open(md_file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    # Удаление оригиналов
    for img_path in processed_images:
        os.remove(img_path)
        print(f"[{target_dir}] Embedded as reference: {img_path.name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dirs", nargs='+')
    args = parser.parse_args()

    for d in args.dirs:
        process_directory(d)
