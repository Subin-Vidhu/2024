# Install nginx on Ubuntu

To check the os:

uname -a

To install nginx:

sudo apt-get install nginx

To check if nginx is installed:

ps -ef | grep nginx

To check whether the service is up and running:

sudo systemctl status nginx

To check nginx version:

nginx -v

To stop nginx:

sudo systemctl stop nginx

To start nginx after stopping:

sudo systemctl start nginx

To validate nginx webserver is running, use curl command[[if curl not found, then : sudo apt install curl], default port: 80]:

$ curl http://localhost/
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
    }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>

check localhost:80 on browser to see this...

# Install nginx on CentOS
[video](https://www.udemy.com/course/nginx-for-sys-and-web-admins-free/learn/lecture/41076624#overview, "Reference")


