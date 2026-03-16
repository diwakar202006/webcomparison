import requests
from bs4 import BeautifulSoup


headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9"
}


def amazon_price(product):

    url = f"https://www.amazon.in/s?k={product.replace(' ','+')}"

    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.text, "html.parser")

    price = soup.select_one(".a-price-whole")

    if price:
        return int(price.text.replace(",",""))
    else:
        return None


def compare_price(product, stores):

    result = {}

    if "amazon" in stores:

        price = amazon_price(product)

        if price:
            result["amazon"] = price
        else:
            result["amazon"] = "Not found"

    if "flipkart" in stores:
        result["flipkart"] = "Coming soon"

    if "myntra" in stores:
        result["myntra"] = "Coming soon"

    if "ajio" in stores:
        result["ajio"] = "Coming soon"

    if "jiomart" in stores:
        result["jiomart"] = "Coming soon"

    return result