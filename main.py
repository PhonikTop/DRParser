import asyncio
import aiohttp
from bs4 import BeautifulSoup


async def fetch_html(url, user_agent=None):
    headers = {"User-Agent": user_agent} if user_agent else {}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return await response.text()


async def get_product_info(url):
    user_agent = (
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0"
    )
    html = await fetch_html(url, user_agent)
    soup = BeautifulSoup(html, "html.parser").find(
        "div", class_="facet__products-list js-facet-product-list"
    )
    container = soup.find_all("div", class_="prd-main-wrapper")
    for obj in container:
        name = obj.find("h3", class_="seo-heading").text.strip()
        autor = obj.find("a", class_="who font-weight-bold").text.strip()
        price = obj.find("div", class_="prd-price").text.strip()
        print(f"{name}\n{autor}\n{price}\n\n")


async def main():
    url = "https://www.dr.com.tr/search?Page=1&Q=Python&SortOrder=1&SortType=0"

    product_info = await get_product_info(url)
    print(product_info)


if __name__ == "__main__":
    asyncio.run(main())
