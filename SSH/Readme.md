#  SSH

 - Secure Shell

 - Protocol to communicate with other computers

 - Do just about anything with the remote server

 - Traffic is encrypted

 - Terminal/Command line

 - Requires SSH and SSHD, where SSH is the client and SSHD is the server.[must have SSHD installed on the server for connection via SSH]

    `````
    sudo apt update
    sudo apt install openssh-server
    sudo systemctl restart sshd
    ssh username@hostname_or_ip_address
    `````

 - Change the sshd_config file for giving permissions

 - Different Authentication Methods

   Password
   
   Public/Private Key Pair

   Host based

 - Generating Keys

   Create public and private key using `ssh-keygen` and add the public key to the server[inside .ssh folder in authorized_keys file]

 - For connecting to the server from Windows, use either Git Bash or Putty

 - Refer Notes and Telegram[2024_Done] for more... 