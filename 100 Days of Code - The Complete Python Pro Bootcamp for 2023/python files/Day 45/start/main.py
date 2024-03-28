from bs4 import BeautifulSoup
# import lxml

with open("Day045/bs4-start/website.html",encoding="utf8") as file:
    contents=file.read()

# let us create a BeautifulSoup object and assigns it to the soup variable
# The BeautifulSoup object assigned to soup is created with two arguments.
# The first argument is the HTML to be parsed, and the second argument, the string "html.parser", tells the object which parser to use behind the scenes. "html.parser" represents Python’s built-in HTML parser.
soup=BeautifulSoup(contents,"html.parser")

# soup=BeautifulSoup(contents,"lxml")

#soup is object that allows us to tap into various parts of website,using python
print(soup.title)
print(soup.title.name)  #name of tag
print(soup.title.string) #actual text within tag


#entire soup object represents html code so printing soup prints all html code
# print(soup)
# print(soup.prettify()) indents html code


#get first <a> tag in our website
print(soup.a)

# to get all <a> tags in our website
all_anchor_tags=soup.find_all(name="a")
print(all_anchor_tags)


for tag in all_anchor_tags:
    #print all text in all anchor tags
    # print(tag.getText())

    #to get actual link in <a> tag
    print(tag.get("href"))

# we can get hold of items using id or class to be more specific 
# eg.if there are a lot of <h1> tags,we can use id

heading=soup.find_all(name="h1",id="name")
print(heading)

#we use class_ instead of class as class in python means a reserved keyword only used for creating classes
h3_heading=soup.find_all(name="h3",class_="heading")
print(h3_heading)

# to get a particular a tag
# we are looking for a tag inside p tag
company_url=soup.select_one(selector="p a")
print(company_url)

name=soup.select_one(selector="#name")
print(name)

headings=soup.select(".heading")
print(headings)