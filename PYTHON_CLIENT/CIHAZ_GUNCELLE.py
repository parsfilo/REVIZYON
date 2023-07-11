from os import system

KOMUTLAR = [
    "pip install --upgrade pip setuptools wheel",
    "pip freeze > requirements.txt",
    "pip install -r requirements.txt --upgrade",
    "rm requirements.txt",
    "sudo raspi-config nonint do_wifi_country TR",
    "sudo apt update",
    "sudo apt upgrade -y",
    "sudo apt update -y",
    "sudo apt autoremove -y",
    "sudo apt upgrade -y",
    "sudo apt autoremove -y",
    "sudo apt dist-upgrade -y",
    "sudo apt clean -y",
    "sudo apt dist-upgrade -y",
    "sudo apt full-upgrade -y",
    "sudo apt autoclean",
    "sudo apt-get dist-upgrade -y",
    "sudo apt --fix-missing update",
    "sudo apt install -f",
    "sudo apt --fix-broken install",
    "sudo apt full-upgrade",
    "sudo apt autoremove -y",
    "sudo apt update",
    "sudo apt upgrade -y",
    "sudo rpi-eeprom-update -d -a",
    # "sudo dpkg-reconfigure tzdata",
    "sudo rpi-update",
    # "sudo reboot",
    "sudo service mongod stop",
    "sudo apt-get purge mongodb-org* -y",
    "sudo rm -r /var/log/mongodb",
    "sudo rm -r /var/lib/mongodb",
    "wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -",
    "echo 'deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse' | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list",
    "sudo apt-get update",
    "sudo apt-get install -y mongodb-org=4.4.8 mongodb-org-server=4.4.8 mongodb-org-shell=4.4.8 mongodb-org-mongos=4.4.8 mongodb-org-tools=4.4.8",
    "sudo systemctl daemon-reload",
    "sudo systemctl enable mongod",
    "sudo systemctl start mongod",
    "sudo systemctl status mongod",
    "sudo npm install -g npm",
    "sudo npm install -g nodemon",
    "sudo npm install -g npm-check-updates",
    "cd /home/pi/Desktop/REVIZYON/NODE_SERVER/;ncu -u;npm install"
    ]

for n in range(len(KOMUTLAR)):
    print("----------------------------------------------------")
    print(KOMUTLAR[n])
    system(KOMUTLAR[n])
    print("----------------------------------------------------")
