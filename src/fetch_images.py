import os
import json
import requests
from PIL import Image
from io import BytesIO
import numpy as np

def fetch_image(file_or_url):
    """Dosya yolundan veya URL'den görsel alır."""
    try:
        if file_or_url.startswith("http"):
            # URL'den görsel çek
            response = requests.get(file_or_url, timeout=5)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content)).convert("RGB")
        else:
            # Dosya yolundan görsel oku
            img = Image.open(file_or_url).convert("RGB")
        img = img.resize((224, 224))  # Görseli yeniden boyutlandır
        return np.array(img)
    except Exception as e:
        print(f"Failed to fetch image {file_or_url}: {e}")
        return None

def process_category(category, image_data):
    """Bir kategorideki tüm görselleri işler."""
    images = []
    if category in image_data:
        for file_or_url in image_data[category]:
            img_array = fetch_image(file_or_url)
            if img_array is not None:
                images.append(img_array)
    return images

def add_healthy_to_json(healthy_dir, json_path):
    """Sağlıklı cilt görsellerini JSON dosyasına ekler."""
    with open(json_path, "r", encoding="utf-8") as f:
        image_data = json.load(f)

    image_data["healthy-skin"] = []
    for filename in os.listdir(healthy_dir):
        if filename.endswith((".jpg", ".jpeg", ".png")):
            image_path = os.path.join(healthy_dir, filename)
            image_data["healthy-skin"].append(image_path)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(image_data, f, indent=4)
    print(f"Sağlıklı cilt görselleri JSON dosyasına eklendi: {json_path}")

if __name__ == "__main__":
    # Sağlıklı görsellerin JSON'a eklenmesi
    add_healthy_to_json("../data/healthy", "../data/image_urls.json")

    # JSON dosyasını yükle ve bir kategoriyi işleyin
    with open("../data/image_urls.json", "r", encoding="utf-8") as f:
        image_data = json.load(f)

    category = "healthy-skin"  # Sağlıklı cilt kategorisi
    images = process_category(category, image_data)
    print(f"Processed {len(images)} images from category '{category}'")
