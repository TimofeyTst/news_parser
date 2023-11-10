from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import json

def scroll_page(driver):
    # Автоматическая прокрутка страницы
    scroll_pause_time = 1
    start_time = time.time()
    max_time = 40
    while (time.time() - start_time) < max_time:  # Прокручиваем в течение 5 минут
        # Прокрутка вниз
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(scroll_pause_time)


def parse_page(driver, ticker):
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find_all('li', class_='js-stream-content Pos(r)')

    data = []
    for item in items:
        source_span = item.find('div', class_='C(#959595)')
        source_name = source_span.find('span') if source_span else None
        source_name = source_name.get_text() if source_name else None

        news_link = item.find('a', class_='js-content-viewer') if item.find('a', class_='js-content-viewer') else None

        if source_name and news_link:
            link = news_link.get('href')
            title = news_link.text
            data.append({'source_name': source_name, 'ticker': ticker, 'title': title, 'link': f"https://finance.yahoo.com{link}"})

    return data

def process_url(url, ticker, driver):
    # Открываем веб-сайт
    driver.get(url)
    # Прокручиваем страницу
    scroll_page(driver)
    # Парсим страницу
    data = parse_page(driver, ticker)

    return data


def main():
    # Список URL для обработки
    urls = [
        'https://finance.yahoo.com/quote/AAPL/news?p=AAPL',
        'https://finance.yahoo.com/quote/PCCYF/news?p=PCCYF',
        'https://finance.yahoo.com/quote/XOM/news?p=XOM',
        'https://finance.yahoo.com/quote/AMZN/news?p=AMZN',
    ]
    with open('test/selenium/yahoo_urls.txt', 'r') as f:
        urls = [url.split() for url in f.readlines()]

    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Список для хранения данных
    all_data = []

    for ticker, url in urls:
        data = process_url(url, ticker, driver)
        all_data.extend(data)

    # Записываем все данные в JSON файл
    with open('data.json', "w", encoding="utf-8") as file:
        json.dump(all_data, file, ensure_ascii=False, indent=4)

    # Завершаем работу браузера
    driver.quit()


if __name__ == "__main__":
    main()
