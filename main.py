import os
import time
import smtplib
from typing import Final
from datetime import datetime as dt
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

FROM_EMAIL: Final[str] = os.getenv('FROM_EMAIL')
PASSWORD: Final[str] = os.getenv('PASSWORD')
TO_EMAIL: Final[str] = os.getenv('TO_EMAIL')

URL: Final[str] ="https://www.amazon.com/Manhattan-Toy-Kodiak-Stuffed-Animal/dp/B0007WJ4VC"
TARGET_PRICE: Final[float] = 310.0

def get_soup() -> BeautifulSoup:
    response = requests.get(URL, headers={
        'Accept-Language': 'en-US,en;q=0.9,he;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    })

    return BeautifulSoup(response.text, 'html.parser')

def get_price(soup: BeautifulSoup) -> float:
    price_whole = soup.find(name="span", class_="a-price-whole")
    price_decimal = soup.find(name="span", class_="a-price-fraction")

    return float(price_whole.text + price_decimal.text)

def send_email(message: str) -> None:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(FROM_EMAIL, PASSWORD)
        connection.sendmail(from_addr=FROM_EMAIL, to_addrs=TO_EMAIL, msg=message)
        connection.quit()

def check_condition() -> None:
    while True:
        now = dt.now()
        if now.hour in [0, 4, 8, 12, 16, 20] and now.minute == 0:
            soup: BeautifulSoup = get_soup()
            price: float = get_price(soup)
            if price <= TARGET_PRICE:
                message: str = f"""Subject: Manhattan-Toy-Kodiak-Stuffed-Animal Amazon Price\nFrom: noreply <{FROM_EMAIL}> \n\n
                Manhattan-Toy-Kodiak-Stuffed-Animal's price went under your target price of ${TARGET_PRICE}!\n
                current price: ${price}
                click here to buy: {URL}
                """
                send_email(message)
                print("sent")
                time.sleep(60)
            else:
                time.sleep(60)
        else:
            time.sleep(60)

if __name__ == "__main__":
    check_condition()