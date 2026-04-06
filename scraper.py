import requests
from bs4 import BeautifulSoup


headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9"
}
def amazon_price(product):

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9"
    }

    url = f"https://www.amazon.in/s?k={product.replace(' ','+')}"

    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.text, "html.parser")

    whole = soup.select_one(".a-price-whole")
    fraction = soup.select_one(".a-price-fraction")

    if whole:
        whole_text = whole.text.replace(",", "").strip()

        if fraction:
            fraction_text = fraction.text.strip()
            full_price = whole_text + fraction_text
        else:
            full_price = whole_text

        return int(full_price)

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