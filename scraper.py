from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def compare_price(product):

    driver = webdriver.Chrome()

    # AMAZON
    driver.get("https://www.amazon.in")

    search = driver.find_element(By.ID,"twotabsearchtextbox")
    search.send_keys(product)
    search.send_keys(Keys.RETURN)

    time.sleep(3)

    amazon_price = driver.find_element(By.CLASS_NAME,"a-price-whole").text

    # FLIPKART
    driver.get("https://www.flipkart.com")

    time.sleep(3)

    try:
        driver.find_element(By.XPATH,"//button[contains(text(),'✕')]").click()
    except:
        pass

    search = driver.find_element(By.NAME,"q")
    search.send_keys(product)
    search.send_keys(Keys.RETURN)

    time.sleep(3)

    flipkart_price = driver.find_element(By.XPATH,"(//div[contains(text(),'₹')])[1]").text

    driver.quit()

    return {
        "amazon": amazon_price,
        "flipkart": flipkart_price
    }