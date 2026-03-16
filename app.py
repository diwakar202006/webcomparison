from flask import Flask, render_template, request
from scraper import compare_price, amazon_price
import json

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():

    result = None

    if request.method == "POST":

        product = request.form["product"]

        stores = request.form.getlist("store")

        result = compare_price(product, stores)

    return render_template("index.html", result=result)


# Track price route
@app.route("/track", methods=["POST"])
def track():

    product = request.form["product"]
    phone = request.form["phone"]

    price = amazon_price(product)

    data = []

    try:
        with open("tracked_products.json","r") as f:
            data = json.load(f)
    except:
        pass

    data.append({
        "product": product,
        "price": price,
        "phone": phone
    })

    with open("tracked_products.json","w") as f:
        json.dump(data,f,indent=4)

    return "Product added for price tracking!"


if __name__ == "__main__":
    app.run(debug=True)