# Ubuntu Network Server

## Commands
Done wrt to the protos system.

1. To list out the hostname.

```
$ hostname
protos
```

2. List all the network interfaces.
```
$ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: enp4s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether d8:5e:d3:d0:72:e5 brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.6/24 brd 192.168.1.255 scope global noprefixroute enp4s0
       valid_lft forever preferred_lft forever
    inet6 fe80::da5e:d3ff:fed0:72e5/64 scope link 
       valid_lft forever preferred_lft forever
3: wlx386b1cd1606b: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc mq state DOWN group default qlen 1000
    link/ether 38:6b:1c:d1:60:6b brd ff:ff:ff:ff:ff:ff
4: br-01fbb90bdfab: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default 
    link/ether 02:42:f9:bc:21:59 brd ff:ff:ff:ff:ff:ff
    inet 172.20.0.1/16 brd 172.20.255.255 scope global br-01fbb90bdfab
       valid_lft forever preferred_lft forever
    inet6 fe80::42:f9ff:febc:2159/64 scope link 
       valid_lft forever preferred_lft forever
5: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN group default 
    link/ether 02:42:4b:25:a7:a3 brd ff:ff:ff:ff:ff:ff
    inet 172.17.0.1/16 brd 172.17.255.255 scope global docker0
       valid_lft forever preferred_lft forever
6: br-d5610e9a573a: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN group default 
    link/ether 02:42:d2:fe:4c:98 brd ff:ff:ff:ff:ff:ff
    inet 172.21.0.1/16 brd 172.21.255.255 scope global br-d5610e9a573a
       valid_lft forever preferred_lft forever
1788: veth61033a8@if1787: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master br-01fbb90bdfab state UP group default 
    link/ether ae:86:56:f4:11:1b brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet6 fe80::ac86:56ff:fef4:111b/64 scope link 
       valid_lft forever preferred_lft forever

```
3. When you want to run something as administrator, use `sudo`

```
$ sudo apt update
```
4. Some common commands.
```
$ ls
$ cd / cd ..
$ pwd
$ cat
$ touch
$ whoami
```
## Remote Access
1. SSH.
```
$ ssh -V
OpenSSH_8.2p1 Ubuntu-4ubuntu0.11, OpenSSL 1.1.1f  31 Mar 2020
```
2. If not found to install use:
```
sudo apt install openssh-server
```
3. To check the status.
```
$ sudo service ssh status
[sudo] password for protos: 
● ssh.service - OpenBSD Secure Shell server
     Loaded: loaded (/lib/systemd/system/ssh.service; enabled; vendor preset: e>
     Active: active (running) since Mon 2024-04-08 08:44:04 IST; 1 day 6h ago
       Docs: man:sshd(8)
             man:sshd_config(5)
    Process: 1096 ExecStartPre=/usr/sbin/sshd -t (code=exited, status=0/SUCCESS)
   Main PID: 1132 (sshd)
      Tasks: 1 (limit: 76906)
     Memory: 4.8M
     CGroup: /system.slice/ssh.service
             └─1132 sshd: /usr/sbin/sshd -D [listener] 0 of 10-100 startups

Apr 09 14:36:13 protos sshd[181726]: Failed password for root from 183.81.169.2>
Apr 09 14:36:13 protos sshd[181726]: Connection closed by authenticating user r>
Apr 09 14:42:28 protos sshd[182297]: pam_unix(sshd:auth): authentication failur>
Apr 09 14:42:30 protos sshd[182297]: Failed password for root from 103.230.121.>
Apr 09 14:42:33 protos sshd[182297]: Connection closed by authenticating user r>
Apr 09 14:43:27 protos sshd[182303]: Invalid user admin from 91.92.243.169 port>
Apr 09 14:43:27 protos sshd[182303]: pam_unix(sshd:auth): check pass; user unkn>
Apr 09 14:43:27 protos sshd[182303]: pam_unix(sshd:auth): authentication failur>
Apr 09 14:43:28 protos sshd[182303]: Failed password for invalid user admin fro>
```
4. Restart.
```
$ sudo service ssh restart
```
5. To enable ssh on system startup.
```
sudo systemctl enable ssh
```
6. To edit the settings, edit the sshd_config file inside etc/ssh/ and then restart ssh using:

```
$ sudo service ssh restart
```
7. To connect from a system with a comman LAN, enter the password if public key is not set[tested using windows]:
```
ssh protos@192.168.1.6
```

## Users
1. To add new user.
```
$ sudo addduser <name>
```
Create a password and leave all as default values.

2. To list out the users
```
$ cd /
$ cd home
$ ls
```

3. To grand super-user privilages to the new user
```
$ sudo usermod -aG sudo <name>
```
4. To change user
``` 
$ su - <name>
```
5. To see file permissions
```
$ ls -l

output eg:
$ ls -l
total 12
drwxr-xr-x 22 celsus celsus 4096 Mar 23 11:13 celsus
drwxr-xr-x 18 chippy chippy 4096 Mar 26 10:19 chippy
drwx------ 38 protos protos 4096 Apr  9 14:52 protos
```
6. To change settings of a file
```
$ chmod u+rw <filename>
$ chmod u-rw <filename>
```
7. To change the owner of a file
```
$ sudo chown <name>:<name> <filename>
```
8. To change the owner of a folder
```
$ chmod 777 <folder>
$ chmod 666 <folder>
```
## File Transfer

1. sftp 
Enable the sftp option in sshd_config
2. Add users 
```
$ sudo groupadd sftpusers
$ sudo usermod -aG sftpusers <name>
$ sudo service ssh restart
```
3. To connect from windows:
```
PS C:\Users\Subin-PC> sftp protos@192.168.1.6

```
4. To Transfer a file:
```
sftp> get transfer_move.txt
```
5. Use WinSCP or FileZilla for transfering with the help of a UI

