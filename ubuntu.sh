grep -r -o -i "bind-address" *

#ufw uncomplicated firewall
sudo ufw allow from any to any port 3306 proto tcp

sudo ufw status
sudo ufw allow XXXX/tcp
# use a port other than the default/predictable 3306
# work outside, and close the door when you are done
sudo ufw deny XXXX/tcp

---
ufw --version

ufw enable

nano /etc/default/ufw

ufw app list

sudo ufw allow OpenSSH

sudo ufw allow ssh

sudo ufw allow 22
sudo ufw allow 5000,3000,3306
sudo ufw allow 2222

sudo ufw show added
