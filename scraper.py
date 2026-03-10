import requests
from bs4 import BeautifulSoup

def compare_price(product):

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    # AMAZON SEARCH
    amazon_url = f"https://www.amazon.in/s?k={product}"

    r = requests.get(amazon_url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    price = soup.select_one(".a-price-whole")

    if price:
        amazon_price = price.text
    else:
        amazon_price = "Not found"

    return {
        "amazon": amazon_price,
        "flipkart": "Coming soon"
    }