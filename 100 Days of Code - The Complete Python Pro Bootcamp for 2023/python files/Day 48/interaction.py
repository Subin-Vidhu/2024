from selenium import webdriver

#To send a key thats not a letter or number or sumbol,we need to import this
from selenium.webdriver.common.keys import Keys

CHROME_DRIVER_PATH="C:\Python_development\chromedriver.exe" #only for windows machine
driver=webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)

WIKIPEDIA_URL="https://en.wikipedia.org/wiki/Main_Page"
driver.get(WIKIPEDIA_URL)

#---------CLICKING ON LINKS--------------------#
#To click on number of articles link
number=driver.find_element_by_css_selector("#articlecount a")
# print(number.text)
# number.click()

#If we wanted to click on 'All portals' link
all_portals=driver.find_element_by_link_text("All portals")
# all_portals.click()

#---------------TYPING-----------------------#
#Searching in wikipedia searchbar
#find the search bar using Chrome inspect tool
search=driver.find_element_by_name("search")
#typing python
search.send_keys('Python')
#Now hit enter key to start searching(need to import)
#From this Keys class,we wish to send one of the constants available there, ENTER
search.send_keys(Keys.ENTER)



driver.quit()