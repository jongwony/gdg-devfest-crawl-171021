#!/usr/bin/env bash

# Only Ubuntu Example
cd /home/ubuntu
git clone https://github.com/lastone9182/gdg-devfest-crawl-171021.git

# Setup Ubuntu Dependencies
# https://stackoverflow.com/questions/26852572/how-to-avoid-grub-errors-after-running-apt-get-upgrade-ubuntu
# man apt, man dpkg
DEBIAN_FRONTEND=noninteractive
apt update
apt -o Dpkg::Options::"--force-downgrade" upgrade -y

# Chrome stable binary(not driver)
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg -i google-chrome-stable_current_amd64.deb
apt install -f -y
rm google-chrome-stable_current_amd64.deb

apt install xvfb build-essential python3-pip -y
pip3 install --upgrade pip

# Install python package
pip3 install -r requirements.txt

# Insert rc.local
# git pull -> script execution
sed -i "$ s/exit 0/cd \/home\/ubuntu\/gdg-devfest-crawl-171021\ngit pull\npython3 example.py --aux\nexit 0/" /etc/rc.local
cat /etc/rc.local
