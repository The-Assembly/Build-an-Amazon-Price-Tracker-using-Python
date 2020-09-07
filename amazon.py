import requests
from bs4 import BeautifulSoup
import smtplib
import csv
import datetime
import os
import time


def send_email():
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login("email","password")

    subject= "Hey! The prices are affordable"
    body = "Go and order now at https://www.amazon.ae/Samsung-Galaxy-Ultra-128GB-Version/dp/B084H8DSCZ/ref=sr_1_6?dchild=1&keywords=samsung+s20&qid=1599291913&sr=8-6"
    msg = f"Subject:{subject}\n\n\n\n{body}"

    server.sendmail("email","email",msg)
    print("email sent")
    server.quit()






url = "https://www.amazon.ae/Samsung-Galaxy-Ultra-128GB-Version/dp/B084H8DSCZ/ref=sr_1_6?dchild=1&keywords=samsung+s20&qid=1599291913&sr=8-6"

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}

def check_price_and_log():
    page = requests.get(url, headers=headers)

    bs = BeautifulSoup(page.content, 'html.parser')

    #print(bs.prettify().encode("utf-8"))

    product_title = bs.find(id = "productTitle").get_text()
    print(product_title.strip())

    product_price = bs.find(id = "priceblock_ourprice").get_text()


    product_price = product_price[4:9]
    print(product_price)

    price_float = float(product_price.replace(",",""))
    print(price_float)

    file_exists = True

    if not os.path.exists("./price.csv"):
        file_exists = False

    with open("price.csv","a") as file:
        writer = csv.writer(file,lineterminator ="\n")
        fields = ["Timestamp","price"]
        
        if not file_exists:
            writer.writerow(fields)

        timestamp = f"{datetime.datetime.date(datetime.datetime.now())},{datetime.datetime.time(datetime.datetime.now())}"
        writer.writerow([timestamp, price_float])
        print("wrote csv data")

    return price_float






while True:
    price = check_price_and_log()
    if(price <= 3200):
        send_email()
        break
    time.sleep(43200)

