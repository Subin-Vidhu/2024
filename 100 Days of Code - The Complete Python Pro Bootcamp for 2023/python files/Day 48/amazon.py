# AMAZON PRICE TRACKER FROM DAY 47 USING SELENIUM WEB TRACKER
from selenium import webdriver

CHROME_DRIVER_PATH="C:\Python_development\chromedriver.exe" #only for windows machine
driver=webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)

#taking product url from Day 047
AMAZON_PRODUCT_URL="https://www.amazon.com/dp/B08PQ2KWHS/ref=sspa_dk_detail_0?psc=1&pd_rd_i=B08PQ2KWHS&pd_rd_w=mk2nj&pf_rd_p=5d846283-ed3e-4512-a744-a30f97c5d738&pd_rd_wg=Rh4OA&pf_rd_r=KR490CN4T7MP03R7TCW0&pd_rd_r=40dba336-d6f7-4d40-b390-dad3b2a440ab&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUFFUEE5UEFZS1NaU0MmZW5jcnlwdGVkSWQ9QTAxODcyNzczUkxTMzdETVJGODU2JmVuY3J5cHRlZEFkSWQ9QTA0MTk1MTMzUkZDN0RDN083VzhKJndpZGdldE5hbWU9c3BfZGV0YWlsX3RoZW1hdGljJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ=="

#opens new window
driver.get(AMAZON_PRODUCT_URL)

#use Chrome inspect and find out by price ID
price=driver.find_element_by_id("priceblock_dealprice")
print(price.text)

#this is much shorter than the Day 47 code  as we are driving the browser
#Browser is already sending all of the headers and information that Amazon expects from an actual user.
#Beautiful Soup is good for scraping data from html website
#but gets stuck if website is of javascript or react and HTML content takes time to load.


#FINDING ELEMENTS BY NAME,USEFUL IN FILLING WEB FORMS WHERE NAME ATTRIBUTE IS USED.
#LET US FIND SEARCH BAR AT TOP OF AMAZON WEB PAGE.
# search_bar=driver.find_element_by_name("field-keywords")
# print(search_bar)
# print(search_bar.tag_name)
# print(search_bar.get_attribute("id"))


driver.quit()