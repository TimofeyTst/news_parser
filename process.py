import os

import aiohttp
from bs4 import BeautifulSoup
from datetime import datetime
from yahoo_parser import YahooParser


class Worker:
    def __init__(self, client, session):
        # self.session = session
        self.client = client
        self.parser = YahooParser(session, self.save)

    async def start(self):
        threads = []

        while True:
            data = await self.client.que.get()
            if data is None:
                await self.client.que.put(None)
                break

            await self.parser.fetch_and_parse(*data)

        for thread in threads:
            thread.join()

    async def fetch_url(self, url):
        try:
            async with self.session.get(url, headers=self.headers) as response:
                return await response.text()
        except aiohttp.client_exceptions.ClientConnectorError as e:
            print(f"\033[91mError connecting to {url}: {e}\033[0m")
        except Exception as e:
            print(f"\033[91mFailed to retrieve the URL '{url}': {e}[0m]")

        return None

    def parse_html(self, html_text):
        soup = BeautifulSoup(html_text, "html.parser")
        text = soup.get_text()

        if self.client.debug:
            result = f"Result: {text[5:7]}"
            print(result)

        return text

    def save(self, src, cat, supcat, text):
        src_id = self.get_or_create_id(src, self.client.sources)
        cat_id = self.get_or_create_id(cat, self.client.categories)
        supcat_id = self.get_or_create_id(supcat, self.client.supercategories)

        file_path = f"data/news/news_{self.client.processed_urls}/news.txt"
        current_time = datetime.now().strftime("%m-%d-%Y %H:%M:%S")

        # Создать директорию, если её нет и сохранить текст новости в файл
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(text)

        text_id = self.client.processed_urls
        self.client.metadata["texts"].append(
            {
                "id": text_id,
                "file_name": file_path,
                "time": current_time,
            }
        )
        self.client.metadata["annotations"].append(
            {
                "text_id": text_id,
                "source_id": src_id,
                "category_id": cat_id,
                "supercategory_id": supcat_id,
            }
        )
        self.client.processed_urls += 1
        print(f"\033[33mTotally urls processed: {self.client.processed_urls}\033[0m")

    @staticmethod
    def get_or_create_id(el, arr):
        if el in arr:
            el_id = arr.index(el)
        else:
            arr.append(el)
            el_id = len(arr) - 1
        return el_id
