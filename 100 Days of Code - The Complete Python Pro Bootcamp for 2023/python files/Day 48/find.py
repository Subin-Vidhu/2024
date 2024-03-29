# finding by name useful in filling forms as when we submit forms,the value in name attribute gets submitted.
from selenium import webdriver

CHROME_DRIVER_PATH="C:\Python_development\chromedriver.exe" #only for windows machine
driver=webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)

PYTHON_ORG_URL="https://www.python.org/"
driver.get(PYTHON_ORG_URL)

#Use Chrome inspect
#FINDING BY NAME
#find the search bar in the Python docs  
# search_bar=driver.find_element_by_name("q")
# print(search_bar.tag_name)
# print(search_bar.get_attribute("placeholder"))

#FINDING BY CLASS NAME 
# logo=driver.find_elements_by_class_name("python-logo")
# When you search for a class, there may be multiple matching elements, so it returns a list of all found matches. Even if you only have a single element with that class, it will still return a list for consistency.
# Just grab the first element from the found elements
# print(logo[0].size)

#OR

#just use find_element_by_class_name to get only the first element
# logo=driver.find_element_by_class_name("python-logo")
# print(logo.size)


#FINDING BY CSS SELECTOR
# documentation_link=driver.find_element_by_css_selector(".documentation-widget a")
# print(documentation_link.text)


#FINDING BY XPATH
#used if we can't get to the element using class or id.
bug_link=driver.find_element_by_xpath('//*[@id="site-map"]/div[2]/div/ul/li[3]/a')
print(bug_link.text)


driver.quit()