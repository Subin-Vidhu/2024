# Install nginx on Ubuntu

## To check the os:

``
uname -a
``

## To install nginx:
``
sudo apt-get install nginx
``
## To check if nginx is installed:
``
ps -ef | grep nginx
``
## To check whether the service is up and running:
``
sudo systemctl status nginx
``
## To check nginx version:
``
nginx -v
``
## To stop nginx:
``
sudo systemctl stop nginx
``
## To start nginx after stopping:
``
sudo systemctl start nginx
``
## To restart nginx:
``
systemctl restart nginx
``
To validate nginx webserver is running, use curl command[[if curl not found, then : sudo apt install curl], default port: 80]:

``````
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
``````
check localhost:80 on browser to see this...

## Install nginx on CentOS
[video](https://www.udemy.com/course/nginx-for-sys-and-web-admins-free/learn/lecture/41076624#overview, "Reference")

## Install nginx on Docker container
[video1](https://www.udemy.com/course/nginx-for-sys-and-web-admins-free/learn/lecture/41076628#overview, "Links")

[video2](https://www.udemy.com/course/nginx-for-sys-and-web-admins-free/learn/lecture/41076632#overview, "Links")

## Configuration path

![image](https://github.com/Subin-Vidhu/2024/assets/85066028/2a305f07-0e7b-4f0f-b881-039b850f6b8d)

``
ls -la /etc/nginx
``

``
more  /etc/nginx/nginx.conf
``

``
more  /run/nginx.pid [to get the process id of nginx and to check : ps -ef | grep 510752 (510752 was the result from previous command)]
``

## To check the number of processors:
``
grep processor /proc/cpuinfo
``
## To check the modules-enabled:
``
ls -la /etc/nginx/modules-enabled/
``
## Log files in Nginx

[Video](https://www.udemy.com/course/nginx-for-sys-and-web-admins-free/learn/lecture/41076646#overview, "Reference")

## Nginx Others

![image-1](https://github.com/Subin-Vidhu/2024/assets/85066028/baa05c0a-fb14-4bba-903f-fb6b208922ec)

[video](https://www.udemy.com/course/nginx-for-sys-and-web-admins-free/learn/lecture/41076650#overview, "Customising...")

## Nginx Serving content Basics

[video](https://www.udemy.com/course/nginx-for-sys-and-web-admins-free/learn/lecture/41076652#overview, "Reference")

## Nginx Serving content solution

sudo su - [to change to root]

[video](https://www.udemy.com/course/nginx-for-sys-and-web-admins-free/learn/lecture/41076656#overview)

## Configure nginx and tomcat

[video](https://www.udemy.com/course/nginx-for-sys-and-web-admins-free/learn/lecture/41076668#overview)

## SSL Setup

[video](https://www.udemy.com/course/nginx-for-sys-and-web-admins-free/learn/lecture/41076678#overview)
