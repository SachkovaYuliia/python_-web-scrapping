# Парсинг новинного сайту для отримання останніх новин
# Вам потрібно створити Python-скрипт, який буде парсити головну сторінку новинного сайту та збирати інформацію про останні новини. Ваш скрипт повинен отримувати заголовки новин, посилання на повний текст новини, дату публікації та короткий опис (якщо він присутній на сторінці).

import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.technewsworld.com/"
response = requests.get(url)

if response.status_code == 200:
    print("Сторінка завантажена успішно!")
else:
    print(f"Помилка! Код статусу: {response.status_code}")
    exit()

soup = BeautifulSoup(response.text, 'html.parser')

news = []

"""
Знаходимо всі div з новинами
"""
articles = soup.find_all('div', class_='col-md-6 equal-story-block')

"""
B кожній статті:
"""
for article in articles:
    try:
        """
        Витягуємо заголовок
        """
        title_tag = article.find('div', class_='more-txt').find('h2')
        title = title_tag.get_text(strip=True) if title_tag else "Заголовок не знайдено"

        """
        Витягуємо посилання
        """
        link_tag = article.find('a', class_='more-pic')
        link = link_tag['href'] if link_tag and 'href' in link_tag.attrs else "Посилання не знайдено"

        """
        Витягуємо короткий опис
        """
        summary_tag = article.find('div', class_='more-txt')
        if summary_tag:
            summary = summary_tag.get_text(strip=True)
            """
            Видаляємо заголовок із короткого опису, якщо він дублюється
            """
            if title in summary:
                summary = summary.replace(title, "").strip()
        else:
            summary = "Короткий опис не знайдено"

        """
        Додаємо новину в список
        """
        news.append({"title": title, "link": link, "summary": summary})
    except Exception as e:
        print(f"Помилка обробки новини: {e}")

"""
Створюємо DataFrame для зберігання новин
"""
df = pd.DataFrame(news)

"""
Зберігаємо дані 
"""
df.to_csv("news.csv", sep=" ", index=False)

print("Новини успішно збережені.")
