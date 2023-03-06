import requests
from bs4 import BeautifulSoup
import smtplib
import os
# import lxml

MY_EMAIL = os.environ.get("MY_EMAIL")
PASSWORD = os.environ.get("PASSWORD")

PRODUCT_URL = "https://www.amazon.com/dp/B0B76KL25D/ref=sspa_dk_detail_0?psc=1&pd_rd_i=B0B76KL25D&pd_rd_w=zjHVa&content-id" \
      "=amzn1.sym.af9528d2-09ba-47ee-b909-59e3022bebe1&pf_rd_p=af9528d2-09ba-47ee-b909-59e3022bebe1&pf_rd_r" \
      "=SXFR4H74YKAJNEMPCACC&pd_rd_wg=XGAN6&pd_rd_r=4aa6082e-df17-4141-ae4b-53c3a99a39ed&s=kitchen&sp_csd" \
      "=d2lkZ2V0TmFtZT1zcF9kZXRhaWw&spLa" \
      "=ZW5jcnlwdGVkUXVhbGlmaWVyPUEyTDVDQUgyTlRVVkNKJmVuY3J5cHRlZElkPUEwNjIzMjE2M0Q4VlpXOTFHOUROOSZlbmNyeXB0ZWRBZElkPU" \
        "EwNTA3NDAzSlBXMjRaSUgwWjg3JndpZGdldE5hbWU9c3BfZGV0YWlsJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ=="
header = {
    "Accept-Language": "en-GB,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                  "Version/16.2 Safari/605.1.15"
}
response = requests.get(
    url=PRODUCT_URL,
    headers=header
)

soup = BeautifulSoup(response.text, "lxml")
product_name = soup.find("span", class_="a-size-large product-title-word-break").get_text()
product_price = soup.find("span", class_="a-offscreen").get_text()
shipping_price = soup.find("span", class_="a-size-base a-color-secondary").get_text()

product_price_whole = float(product_price.split("$")[1])
target_price = product_price_whole - (product_price_whole * 0.2)

if product_price_whole >= target_price:
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs="send to address",
                            msg=f"Subject:Amazon Alert Price\n\n "
                                f"{product_name}\n"
                                f"${product_price}\n"
                                f"{shipping_price}\n"
                                f"{PRODUCT_URL}")
