import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from urllib.request import urlretrieve

url = "https://ru.wikipedia.org/wiki/%D0%9A%D0%BE%D1%88%D0%BA%D0%B0"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    content_div = soup.find("div", class_="mw-content-ltr")

    if content_div:
        img_tags = content_div.find_all("img")

        os.makedirs("cats", exist_ok=True)

        for img_tag in img_tags:
            img_url = img_tag.get("src")

            img_url = urljoin(url, img_url)

            img_filename = os.path.basename(urlparse(img_url).path)

            try:
                response = requests.get(img_url)
                if response.status_code == 200:
                    with open(os.path.join("cats", img_filename), "wb") as f:
                        f.write(response.content)
                    print(f"Загружен: {img_filename}")
                else:
                    print(f"Ошибка при загрузке: {img_url}")
            except Exception as e:
                print(f"Ошибка: {e}")
    else:
        print("Не получилось найти <div> с классом 'mw-content-ltr' на странице")
else:
    print(f"Не удалось вернуть html, код ответа: {response.status_code}")