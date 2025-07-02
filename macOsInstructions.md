# MAGIS Magnetometer Trolley: Server Setup for macOS

Mac and Linux share a lot of commands together but I created this guide for easier instructions, instead of Googling what the equivalent of each command is. 

Make sure you've downloaded a recent version of Python! Here's the Python website and the releases for macOS. [Python.org] (https://www.python.org/downloads/macos/)

It is recommended that you also install Homebrew (for package managing). You will need it to download mosquitto. It will ask you for a few other steps. 
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
To check if it's installed:
```
brew --version
```
Now, clone the repository
```
$ cd ~/
$ git clone git@github.com:jbkowalkowski/Magnetometer.git [-b branch_name]
```

A virtual environment is needed to run the servers. 
```
python3 -m venv ~/Magnetometer/python/magserv
```
Now activate it
```
source ~/Magnetometer/python/magserv/bin/activate
```
Packages are important!
```
pip3 install paho-mqtt
```
Installing mosquitto from Homebrew
```
brew install mosquitto
brew services start mosquitto
```
Check if mosquitto is installed and running
```
mosquitto -v
```
It will return something like:
```
1683395033: mosquitto version 2.0.15 running
```
To enable remote access to mosquitto broker, run the following command to open the mosquitto.conf file
``
nano /opt/homebrew/etc/mosquitto/mosquitto.conf
```
Move to the end of the file using arrow keys and paste the following two lines:
```
listener 1883
allow_anonymous true
```
Press <code>Ctrl+O</code> to save then <code>Enter</code> and <code>Ctrl+X</code> to exit
Restart mosquitto for the changes to take effect
```
brew services restart mosquitto
```











