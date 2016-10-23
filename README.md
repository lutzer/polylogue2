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
    boxpi1: 192.168.72.3
    boxpi2: 192.168.72.4
    boxpi3: 192.168.72.5
    ```

* disable bluetooth to save power:

  * add to file: `sudo nano /etc/modprobe.d/raspi-blacklist.conf`

    ```
    ##wifi
    #blacklist brcmfmac
    #blacklist brcmutil
    ##bt
    blacklist btbcm
    blacklist hci_uart
    ```

* pull repo: `git clone https://github.com/lutzer/polylogue2.git`

* python packages
  * `sudo pip2 install pyglet && sudo pip2 install socketio-client `

* copy configs: `cp src/box/config.default.py config.py`

* for boxes:
  * autostart script afterdesktop loads, change file: `sudo nano ~/.config/lxsession/LXDE-pi/autostart `
  * add line: `@/usr/bin/python2 /home/pi/polylogue2/src/box/main.py`
  * disable power off screen: edit `sudo nano /etc/lightdm/lightdm.conf` set `xserver-command=X -s 0 dpms`
  * install font: copy perfect dos font to **/usr/share/fonts**`
  * follow **Thermal printer setup**

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




## Thermal Printer setup for Pi3

* disable serial console: `sudo raspi-config` -> Advanced Options -> Serial -> disable
* enable part: `sudo nano /boot/config.txt`, change line: `enable_uart=1`
* disable console:  `sudo systemctl stop serial-getty@ttyS0.service && sudo systemctl disable serial-getty@ttyS0.service `

## Font generation

- font generation by SpriteFontBuilder for mac
- conversion with this script: [https://github.com/playcanvas/fonts/blob/master/fnt_to_json.py](https://github.com/playcanvas/fonts/blob/master/fnt_to_json.py)


## TODO



* drucker anschliessen und steuerung
* feedback dialog auf bildschirm
* fragen auf boxen verteilen
* app fix reconnection bug

