import asyncio
import aiohttp
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


async def fetch_html(url, user_agent=None):
    headers = {"User-Agent": user_agent} if user_agent else {}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()  # добавляем для обработки ошибок
                return await response.text()
        except aiohttp.ClientError as e:
            print(f"Error during HTTP request: {e}")
            return None


async def get_product_info(url):
    user_agent = UserAgent().random
    html = await fetch_html(url, user_agent)
    if html:
        soup = BeautifulSoup(html, "html.parser").find(
            "div", class_="facet__products-list js-facet-product-list"
        )
        if soup:
            container = soup.find_all("div", class_="prd-main-wrapper")
            for obj in container:
                name = obj.find("h3", class_="seo-heading").text.strip()
                author = obj.find(
                    "a", class_="who font-weight-bold"
                ).text.strip()  # изменяем название переменной на author
                price = obj.find("div", class_="prd-price").text.strip()
                product_info = f"{name}\n{author}\n{price}\n\n"
                print(product_info)  # выводим информацию о продукте
        else:
            print(
                "Unable to find product list on the page"
            )  # обрабатываем случай, когда контейнер продуктов не найден
    else:
        print(
            "Failed to fetch HTML from the URL"
        )  # обрабатываем случай, когда HTML не был получен


async def main():
    url = "https://www.dr.com.tr/search?Page=1&Q=Python&SortOrder=1&SortType=0"
    await get_product_info(url)


if __name__ == "__main__":
    asyncio.run(main())
