import tensorflow as tf
import json
from fetch_images import process_category

# JSON dosyasını yükle
with open("../data/image_urls.json", "r", encoding="utf-8") as f:
    image_data = json.load(f)

# Tüm kategorilerden görselleri işleyin
def process_all_categories(image_data):
    """Tüm kategorilerdeki görselleri işler."""
    all_images = []
    all_labels = []
    for label, (category, file_or_urls) in enumerate(image_data.items()):
        print(f"Processing category: {category}")
        category_images = process_category(category, image_data)
        all_images.extend(category_images)
        all_labels.extend([label] * len(category_images))
    return tf.convert_to_tensor(all_images), tf.convert_to_tensor(all_labels)

# Görselleri ve etiketleri işle
images, labels = process_all_categories(image_data)

# TensorFlow Dataset oluştur
dataset = tf.data.Dataset.from_tensor_slices((images, labels))
dataset = dataset.shuffle(len(images)).batch(32)

# Basit bir CNN modeli oluştur
model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(len(image_data), activation='softmax')  # Kategori sayısı kadar çıktı
])

# Modeli eğit
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(dataset, epochs=10)

# Modeli .h5 formatında kaydet
model.save("../models/skin_disease_model.h5")
print("Model saved to '../models/skin_disease_model.h5'")
