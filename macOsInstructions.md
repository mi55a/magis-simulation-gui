# MAGIS Magnetometer Trolley: Server Setup for macOS

Mac and Linux share a lot of commands together but I created this guide for easier instructions, instead of Googling what the equivalent of each command is. 

Make sure you've downloaded a recent version of Python! Here's the Python website and the releases for macOS. [Python.org](https://www.python.org/downloads/macos/)

It is recommended that you also install Homebrew (for package managing). You will need it to download mosquitto. It will ask you for a few other steps. 
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
To check if it's installed:
```
brew --version
```
## Clone the Repository
```
cd ~/
git clone git@github.com:jbkowalkowski/Magnetometer.git [-b branch_name]
```
## Configure a Python Environment
A virtual environment is needed to run the servers. 
```
python3 -m venv ~/Magnetometer/python/magserv
```
Now activate it
```
source ~/Magnetometer/python/magserv/bin/activate
```
### Install the Packages
Packages are important!
```
pip3 install paho-mqtt
```
## Install Mosquitto
I recommend opening another Terminal window for this. Now, we'll install mosquitto from Homebrew
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
### Enable Remote Access to Mosquitto Broker
To enable remote access to mosquitto broker, run the following command to open the mosquitto.conf file.
```
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

Before running the scripts, you'll want to make sure to edit magsys.service and start_combo.sh with your specific information.

In magsys.service, you want to change the following:
```
User=pi
Group=pi
ExecStart=/home/pi/Magnetometer/python/start_combo.sh
```
Instead of pi, put your username. If you don't remember your username, type <code>whoami</code> in another Terminal page. Replace ExecStart with the path to start_combo.sh. If you have VSCode, right click and click "Copy Path"

In start_combo.sh, you want to change the following:
```
export H=/home/pi -> export H=/Users/yourusername
```
You can either:

Run the data simulation (to test MQTT + data flow with fake data), or

Launch the GUI with real hardware, once the Magnetometer is connected.

For the data simulation:
Execute the macOS-specific script for running the simulation
```
chmod +x run_simulation_macos.sh
./run_simulation_macos.sh
```
For the actual application:
```
python3 trolley_data_sub2.py
python3 magnetometer_gui.py

```