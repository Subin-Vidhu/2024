from selenium import webdriver

CHROME_DRIVER_PATH="C:\Python_development\chromedriver.exe" #only for windows machine
driver=webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)

WIKIPEDIA_URL="https://en.wikipedia.org/wiki/Main_Page"
driver.get(WIKIPEDIA_URL)

number=driver.find_element_by_css_selector("#articlecount a")
print(number.text)

driver.quit()