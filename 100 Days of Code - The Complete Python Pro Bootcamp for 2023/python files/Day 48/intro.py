from selenium import webdriver

CHROME_DRIVER_PATH="C:\Python_development\chromedriver.exe" #only for windows machine
driver=webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)

# Selenium can interact with many browsers
# Now,we need to ensure Selenium knows how to handle specifically the Chrome browser
# Hence,chrome driver provides sort of a bridge between selenium and chrome 
# so that,selenium knows how to handle Chrome.

#opens new window
driver.get("https://www.amazon.com")

#If only one tab is open,driver.close() will close that tab.
# driver.close()

#If more than one tab is open,quit will close down all tabs
driver.quit()