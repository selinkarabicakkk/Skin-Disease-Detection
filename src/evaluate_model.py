from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import os
import json

def load_and_prepare_image(image_path):
    """Görseli yükleyip, modele uygun hale getirir."""
    img = Image.open(image_path).convert("RGB")
    img = img.resize((224, 224))  # Modelin girdi boyutuna göre yeniden boyutlandır
    img_array = np.array(img) / 255.0  # Görseli normalize et
    img_array = np.expand_dims(img_array, axis=0)  # Batch boyutu ekle
    return img_array

# 1. JSON dosyasını yükle ve kategori isimlerini al
with open("../data/image_urls.json", "r", encoding="utf-8") as f:
    image_data = json.load(f)
categories = list(image_data.keys())  # Tüm kategori isimleri

# 2. Eğitilmiş modeli yükle
model = load_model("../models/skin_disease_model.h5")  # HDF5 formatında

# 3. Test klasöründeki tüm görselleri işle
test_images_dir = "../data/test_images"
for filename in os.listdir(test_images_dir):
    image_path = os.path.join(test_images_dir, filename)
    if not filename.endswith((".jpg", ".jpeg", ".png")):
        continue

    # Görseli işle ve modele tahmin yaptır
    test_image = load_and_prepare_image(image_path)
    predictions = model.predict(test_image)
    predicted_class = np.argmax(predictions)  # En olası sınıf
    confidence = predictions[0][predicted_class]  # Güven skoru

    # Tahmini kategoriye eşleştir
    predicted_category = categories[predicted_class]

    # Sonuçları yazdır
    print(f"Image: {filename}")
    if predicted_category == "healthy-skin":
        print(f"Prediction: HEALTHY (Confidence: {confidence:.2f})\n")
    else:
        print(f"Prediction: {predicted_category.upper()} (Confidence: {confidence:.2f})\n")
