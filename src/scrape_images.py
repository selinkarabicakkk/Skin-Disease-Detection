# import os
# import requests
# from selenium import webdriver
# from bs4 import BeautifulSoup
# import time

# # Selenium ayarları
# options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Tarayıcıyı arka planda çalıştır
# driver = webdriver.Chrome(options=options)

# # Ana URL
# base_url = "https://dermnetnz.org"
# driver.get(f"{base_url}/images")
# time.sleep(3)

# # Galleries butonunu tetikleyin
# driver.execute_script("document.body.classList.add('collections-visible');")
# time.sleep(2)

# # Sayfanın sonuna kadar kaydır
# def scroll_to_bottom(driver):
#     last_height = driver.execute_script("return document.body.scrollHeight")
#     while True:
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(2)
#         new_height = driver.execute_script("return document.body.scrollHeight")
#         if new_height == last_height:
#             break
#         last_height = new_height

# scroll_to_bottom(driver)

# # Güncellenmiş HTML'yi al
# soup = BeautifulSoup(driver.page_source, "html.parser")

# # Kategori bağlantılarını topla
# categories = soup.find_all("a", href=True)
# category_links = [base_url + cat["href"] for cat in categories if "/images/" in cat["href"]]
# print(f"Found {len(category_links)} categories.")

# # Verilerin kaydedileceği klasör
# output_dir = "data/raw"
# os.makedirs(output_dir, exist_ok=True)

# # Her kategori bağlantısını ziyaret et ve görselleri indir
# for link in category_links:
#     driver.get(link)
#     time.sleep(3)  # Sayfanın yüklenmesi için bekle
#     category_soup = BeautifulSoup(driver.page_source, "html.parser")
    
#     # Hastalık adını belirle
#     category_name = link.split("/")[-1]
#     category_dir = os.path.join(output_dir, category_name)
#     os.makedirs(category_dir, exist_ok=True)
    
#     # Görselleri bul ve indir
#     images = category_soup.find_all("img", class_="[ js-gallery-image ]")
#     print(f"Found {len(images)} images in category: {category_name}")
    
#     for img in images:
#         img_url = base_url + img["src"] if not img["src"].startswith("http") else img["src"]
#         try:
#             img_data = requests.get(img_url).content
#             img_name = os.path.join(category_dir, img_url.split("/")[-1])
#             with open(img_name, "wb") as f:
#                 f.write(img_data)
#             print(f"Saved: {img_name}")
#         except Exception as e:
#             print(f"Failed to download image {img_url}: {e}")

# # Tarayıcıyı kapat
# driver.quit()


import json
from selenium import webdriver
from bs4 import BeautifulSoup
import time

# Selenium ayarları
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Tarayıcıyı arka planda çalıştır
driver = webdriver.Chrome(options=options)

# Ana URL
base_url = "https://dermnetnz.org"
driver.get(f"{base_url}/images")
time.sleep(3)

# Galleries butonunu tetikleyin
driver.execute_script("document.body.classList.add('collections-visible');")
time.sleep(2)

# Kategori bağlantılarını topla
def scroll_to_bottom(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

scroll_to_bottom(driver)

soup = BeautifulSoup(driver.page_source, "html.parser")
categories = soup.find_all("a", href=True)
category_links = [base_url + cat["href"] for cat in categories if "/images/" in cat["href"]]
print(f"Found {len(category_links)} categories.")

# Görsel URL'lerini toplamak
image_data = {}

for link in category_links:
    driver.get(link)
    time.sleep(3)
    category_soup = BeautifulSoup(driver.page_source, "html.parser")
    
    category_name = link.split("/")[-1]
    image_data[category_name] = []
    
    images = category_soup.find_all("img", class_="[ js-gallery-image ]")
    for img in images:
        img_url = base_url + img["src"] if not img["src"].startswith("http") else img["src"]
        image_data[category_name].append(img_url)

# Tarayıcıyı kapat
driver.quit()

# JSON dosyasına kaydet
with open("image_urls.json", "w", encoding="utf-8") as f:
    json.dump(image_data, f, indent=4)
print("Image URLs saved to 'image_urls.json'")
