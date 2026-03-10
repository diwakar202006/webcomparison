import requests
from bs4 import BeautifulSoup

def compare_price(product):

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9"
    }

    url = f"https://www.amazon.in/s?k={product.replace(' ','+')}"

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    # find all prices
    prices = soup.select(".a-price-whole")

    if prices:
        amazon_price = prices[0].text.strip()
    else:
        amazon_price = "Price not found"

    return {
        "amazon": amazon_price,
        "flipkart": "Coming soon"
    }


if __name__ == "__main__":
    product = input("Enter product name: ")
    result = compare_price(product)
    print(result)