from flask import Flask, render_template, request
from scraper import compare_price

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():

    result = None

    if request.method == "POST":
        product = request.form["product"]
        result = compare_price(product)

    return render_template("index.html", result=result)

app.run()