import requests
import lxml
from bs4 import BeautifulSoup
import smtplib
from dotenv import load_dotenv 
import os

MY_EMAIL=os.getenv('MY_EMAIL')
PASSWORD=os.getenv('PASSWORD')

###<<<STEP 1:Use Beautiful Soup to get price of item from Amazon>>>>####
AMAZON_PRODUCT_URL = "https://www.amazon.com/dp/B08PQ2KWHS/ref=sspa_dk_detail_0?psc=1&pd_rd_i=B08PQ2KWHS&pd_rd_w=mk2nj&pf_rd_p=5d846283-ed3e-4512-a744-a30f97c5d738&pd_rd_wg=Rh4OA&pf_rd_r=KR490CN4T7MP03R7TCW0&pd_rd_r=40dba336-d6f7-4d40-b390-dad3b2a440ab&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUFFUEE5UEFZS1NaU0MmZW5jcnlwdGVkSWQ9QTAxODcyNzczUkxTMzdETVJGODU2JmVuY3J5cHRlZEFkSWQ9QTA0MTk1MTMzUkZDN0RDN083VzhKJndpZGdldE5hbWU9c3BfZGV0YWlsX3RoZW1hdGljJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ=="
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

response = requests.get(url=AMAZON_PRODUCT_URL, headers=headers)
soup = BeautifulSoup(response.text, "lxml")

price=soup.select("#priceblock_dealprice")
p=(price[0].getText())
# print(p)
price_without_currency=float(p.strip('$'))
# print(price_without_currency)


####<<<<STEP 2:Send email when price of item falls below our target price,which will be 100 in this case>>>>####
target_price=float(100)
# for testing purposes
# target_price=float(200) 
if price_without_currency<target_price:
    #send an email to ourselves

    connection=smtplib.SMTP("smtp.gmail.com", port=587)
    connection.starttls()#encrypts message so other ppl can't read
    connection.login(user=MY_EMAIL,password=PASSWORD)

    # In the email, include the title of the product, the current price and a link to buy the product.
    product_title=soup.select("#productTitle")[0].getText()
    product_title=(product_title.strip("\n"))
    message=f"Subject:Amazon Price Alert\n\n{product_title} is now ${price_without_currency}\n{AMAZON_PRODUCT_URL}"

    connection.sendmail(
        from_addr=MY_EMAIL,
        to_addrs=MY_EMAIL,
        msg=message
    )

    connection.close()