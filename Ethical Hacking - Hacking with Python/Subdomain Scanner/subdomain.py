
import requests 
import sys 

sub_list = open("wordlist.txt").read() 
subdomains = sub_list.splitlines()

for sub in subdomains:
    sub_domain = f"http://{sub}.{sys.argv[1]}" 
    # print(sub_domain)
 
    try:
        requests.get(sub_domain)
    except requests.ConnectionError: 
        pass
    else:
        print("Found: ",sub_domain) 

