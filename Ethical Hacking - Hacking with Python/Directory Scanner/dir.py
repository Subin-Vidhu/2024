
import requests 
import sys 

sub_list = open("wordlist.txt").read() 
directories = sub_list.splitlines()

for dir in directories:
    dir_enum = f"https://{sys.argv[1]}/{dir}" #.html"
    # print(dir_enum)

    r = requests.get(dir_enum)
    if r.status_code==404: 
        pass
    else:
        print("Valid directory:" ,dir_enum)


