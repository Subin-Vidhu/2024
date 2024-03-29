from selenium import webdriver
from selenium.webdriver.common.keys import Keys

CHROME_DRIVER_PATH="C:\Python_development\chromedriver.exe" #only for windows machine
driver=webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)

SIGN_UP_URL="http://secure-retreat-92358.herokuapp.com/"

driver.get(SIGN_UP_URL)

first_name=driver.find_element_by_name("fName")
first_name.send_keys("Angela")
# first_name.send_keys(Keys.TAB)    (not needed)


last_name=driver.find_element_by_name("lName")
last_name.send_keys("Yu")
# last_name.send_keys(Keys.TAB)     (not needed)


my_email=driver.find_element_by_name("email")
my_email.send_keys("xyz@gmail.com")
# my_email.send_keys(Keys.TAB)       (not needed)


# signup_button=driver.find_element_by_class_name("btn.btn-lg.btn-primary.btn-block") also correct
signup_button=driver.find_element_by_css_selector(".btn.btn-lg.btn-primary.btn-block")
signup_button.click()


# driver.quit() 