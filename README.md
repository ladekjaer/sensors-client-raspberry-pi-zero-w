# Sensors Client for Raspberry Pi Zero W

This little piece of software install on a *Raspberry Pi Zero W*. It reads from any/all connected DS18B20 temperature sensors and sends this data to the chosen 'sensors-api' server.

## Setting up a Raspberry Pi
NB: Remember to set time zone!

To prepare the Raspberry Pi for 'sensors-client' first acquire and install the Raspberry Pi OS. It is easiest obtainable through https://www.raspberrypi.com/software/. By pressing *Ctrl-Shift-X* before writing to the SD Card you will be able to later skip the steps concerning SSH, WiFi and Time Zone.


### Enable SSH
In the `boot` folder on the SD card from with the RPi run, there should be placed an empty file called `ssh` before first boot. This will enabled SSH. The file will be deleted automatically.

On the boot partition on the RPi SD run
```sh
$ touch ssh
```

### Enable WiFi
In the `boot` folder on the SD card from with the RPi run, place a file called `wpa_supplicant.conf` with SSID and key. See https://www.raspberrypi.com/documentation/computers/configuration.html#setting-up-a-headless-raspberry-pi for example. `2 letter ISO 3166-1 country code` can be found on [Wikipedia](https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes). For Denmark it is `DK`.

The file left in the `boot` folder will automatically be deleted after copied to `/etc/wpa_supplicant/wpa_supplicant.conf`.

### Set Time Zone
Open the config
```sh
$ sudo raspi-config
```
Pick `LoLocalisation Options` and there after `Change Time Zone`.

### Add SSH public key to `authorized_keys` (Optional)
Add your SSH public key as a line in
```sh
/home/pi/.ssh/authorized_keys
```
If the file does not exists, just create it.

### Update the system
```sh
$ sudo apt update
$ sudo apt upgrade
```

### Install `pip`
```sh
$ sudo apt install python3-pip
```

### pinout
Install GPIO Zero
```sh
$ pip3 install gpiozero
```
Pinout can now be show by
```sh
$ pinout
```

## Installing sensors
* Put `sensors.py` in `/home/pi/sensors/`
* Update `URL` and `SENSORS_API_KEY` in `sensors.service`
* Copy `sensors.service` to `/etc/systemd/system/` (or make a link: `sudo ln -s /home/pi/sensors/sensors.service /etc/systemd/system/sensors.service`)
* Run as root
	* `systemctl daemon-reload`
	* `systemctl enable sensors`
	* `systemctl start sensors`

## Managing sensors
Use `systemctl` and `journalctl`
