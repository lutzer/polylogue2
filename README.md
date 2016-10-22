# Polylogue2

An interactive installation for biennale 2016

## Install

### Requirements

* src/server: `npm install`
* src/box: `pip install socketio-client && pip install pyglet`
* src/keyboard: `pip install socketio-client && pip install pyglet` 




## PI Installation

* install RASPBIAN JESSIE WITH PIXEL

* standard login: **pi/raspberry**

* change password: `passwd`

* change config: `sudo raspi-config`
  * change keyboard layout
  * change to login with user pi at startup

* update apt: `sudo apt-get update`

* change hostname, edit hostname in  `sudo nano /etc/hosts` and `sudo nano /etc/hostname`
  * hostnames: **keyboardpi**, **boxpiX**

* setup wlan
  * connect to polylogue2 wifi and setup static ip address 
  * or simply plugin ethernet cable
  * ```
    keyboardpi: 192.168.72.2
    boxpi1: 192.168.72.11
    boxpi2: 192.168.72.12
    ...
    ```

* pull repo: `git clone https://github.com/lutzer/polylogue2.git`

* python packages
  * `sudo pip2 install pyglet && sudo pip2 install socketio-client `

* copy configs: `cp src/box/config.default.py config.py`

* for boxes:
  * autostart script afterdesktop loads, change file: `sudo nano ~/.config/lxsession/LXDE-pi/autostart `
  * add line: `@/usr/bin/python2 /home/pi/polylogue2/src/box/main.py`
  * disable power off screen: edit `sudo nano /etc/kbd/config` set `BLANK_TIME=0`
  * install font: copy perfect dos font to **/usr/share/fonts**

* for keyboard

  * add package source for node: `curl -sL https://deb.nodesource.com/setup_4.x | sudo -E bash -`
  * install npm and node:  `sudo apt-get install nodejs`
  * install pm2: `npm install -g pm2`
  * install dependencies, go to dir **src/keyboard/socket**, type: `npm install`
  * setup pm2
    * `sudo pm2 startup systemd -u pi`
    * `pm2 start src/keyboard/socket/main.js --name keyboardSocketServer`
    * `pm2 save`
  * autostart keyboard grabber:
    * add line to .bashrc: `/usb/bin/python2 /home/pi/polylogue2/src/keyboard/keygrabber/main.py`
  * press ESC twice to exit keygrabber


## Router Config

* dhcp adress reservation for keyboardpi on 192.168.72.2





## TODO



* app: nachrichten only unicode
* drucker anschliessen und steuerung
* feedback dialog auf bildschirm
* fragen auf boxen verteilen

