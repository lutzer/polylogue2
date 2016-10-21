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
* setup wlan
  * connect to polylogue2 wifi and setup static ip address 
* pull repo: `git clone https://github.com/lutzer/polylogue2.git`
* python packages
  * `sudo pip2 install pyglet && sudo pip2 install socketio-client `
* copy configs: `cp src/box/config.default.py config.py`
* for boxes:
  * autostart script afterdesktop loads, change file: `sudo nano ~/.config/lxsession/LXDE-pi/autostart `
  * add line: `@/usr/bin/python2 /home/pi/polylogue2/src/box/main.py`
  * disable power off screen: edit `sudo nano /etc/kbd/config` set `BLANK_TIME=0`
  * install font: copy perfect dos font to **/usr/share/fonts**