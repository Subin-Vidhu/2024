from selenium import webdriver

CHROME_DRIVER_PATH="C:\Python_development\chromedriver.exe" #only for windows machine
driver=webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)

PYTHON_ORG_URL="https://www.python.org/"
driver.get(PYTHON_ORG_URL)

#this will give us list of 5 times as we are using find_elements_by_css_selector
#if we used find_element_by_css_selector,it would return only the first element
time_elements=(driver.find_elements_by_css_selector(".event-widget .menu li time"))
# for value in time_elements:
#     print(value.text)
name_elements=(driver.find_elements_by_css_selector(".event-widget .menu li a"))


# using nested dictionary comprehension
events={
    index:{'time':time_elements[x].text,'name':name_elements[x].text} 
    for index in range(0,6)
    for x in range(len(time_elements)) 
}

print(events)

driver.quit()