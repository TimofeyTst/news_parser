import aiohttp
from bs4 import BeautifulSoup

from abstract_parser import Parser, TICKERS


# Занимается парсингом всех новостей источника Yahoo
# для указанной ссылки на компанию проходит по всем новостям
# и отправляет в self.callback
class YahooParser(Parser):
    def __init__(self, session=None, callback=None):
        super().__init__(session, callback)
        self.root = "https://finance.yahoo.com"

    async def fetch_and_parse(self, src, cat, supcat, url):
        # news_list = await self.fetch_url(url)
        # if news_list is None:
        #     return
        # # Далее нужно из response достать все url из li
        # links = self.parse_news_links(news_list)
        # for news_link in links:
        #     news = await self.fetch_url(news_link)
        #     if news is None:
        #         continue
        #     news_text = self.parse_news_text(news)
        #     self.callback(src, cat, supcat, news_text)
        news = await self.fetch_url(url)
        news_text = self.parse_news_text(news)
        self.callback(src, cat, supcat, news_text)

    async def fetch_url(self, url):
        try:
            async with self.session.get(url, headers=self.headers) as response:
                return await response.text()
        except aiohttp.client_exceptions.ClientConnectorError as e:
            print(f"\033[91mError connecting to {url}: {e}\033[0m")
        except Exception as e:
            print(f"\033[91mFailed to retrieve the URL '{url}': {e}[0m]")

        return None

    def parse_news_links(self, html_text):
        soup = BeautifulSoup(html_text, "html.parser")
        news_links = []

        # Находим все элементы li с классом "js-stream-content Pos(r)"
        news_items = soup.find_all("li", class_="js-stream-content Pos(r)")

        for item in news_items:
            # Проверяем, содержит ли элемент метку "Ad"
            if item.select_one("div div div div a:contains('Ad')"):
                continue

            # Ищем ссылку внутри элемента
            link = item.select_one("div div div div h3 a")
            if link:
                news_links.append(self.root + link["href"])

        return news_links

    def parse_news_text(self, html_text):
        soup = BeautifulSoup(html_text, "html.parser")

        # Ищем заголовок новости
        title = soup.select_one("h1")
        if title:
            news_title = title.text.strip()
        else:
            news_title = ""

        # Ищем тело новости
        body = soup.select(
            "div article div div div div div div.caas-content-wrapper > div.caas-body"
        )

        # Извлекаем текст из каждого элемента p и объединяем его
        news_content = "\n\n".join([p.text.strip() for p in body])

        return news_title + "\n\n" + news_content

    def gen_urls(self, file_path):
        source = "Yahoo"
        category = "Investments"
        with open(file_path, "w", encoding="utf-8") as file:
            for ticker in TICKERS.split():
                url = f"{self.root}/quote/{ticker}/news?p={ticker}"
                line = f"{source} {category} {ticker} {url}\n"
                file.write(line)


if __name__ == "__main__":
    yp = YahooParser()
    yp.gen_urls("data/yahoo_urls.txt")
