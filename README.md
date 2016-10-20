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

* create new user: `sudo adduser poly`

  * set sudo permissions `sudo visudo` 
  * add line `poly ALL=(ALL:ALL) ALL`

* change config: `sudo raspi-config`

* setup wlan

  * ​

* pull repo: `git clone https://github.com/lutzer/polylogue2.git`

* python packages

  * `sudo pip2 install pyglet && sudo pip2 install socketio-client `

  ​