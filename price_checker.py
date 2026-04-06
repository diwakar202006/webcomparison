from app import app, db, Product
from scraper import amazon_price
import pywhatkit


def send_whatsapp(phone, message):
    pywhatkit.sendwhatmsg_instantly(
        phone,
        message,
        wait_time=10,
        tab_close=True
    )


with app.app_context():

    products = Product.query.all()

    for item in products:

        print(f"Checking {item.product}...")

        new_price = amazon_price(item.product)

        if new_price is None:
            print("Could not fetch price")
            continue

        print(f"Old: {item.price}, New: {new_price}")

        if new_price < item.price:

            print("Price dropped! Sending alert...")

            message = f"""
📉 Price Drop Alert!

Product: {item.product}

Old Price: ₹{item.price}
New Price: ₹{new_price}

Check Amazon now!
"""

            send_whatsapp(item.phone, message)

            # update price in DB
            item.price = new_price

    db.session.commit()