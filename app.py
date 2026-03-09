from flask import Flask, render_template, request
from scraper import compare_price
import os

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():

    result = None

    if request.method == "POST":
        product = request.form["product"]
        result = compare_price(product)

    return render_template("index.html", result=result)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)