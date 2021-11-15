# Sensors Client for Raspberry Pi Zero W

This little piece of software install on a *Raspberry Pi Zero W*. It reads from any/all connected DS18B20 temperature sensors and sends this data to the chosen 'sensors-api' server.

## Content
* [Preparing a Raspberry Pi](#preparing-a-raspberry-pi)
	* [Enable SSH](#enable-ssh)
	* [Enable WiFi](#enable-wifi)
	* [Set System Time](#set-system-time)
	* [Add SSH public key to `authorized_keys` (Optional)](#add-ssh-public-key-to-authorized_keys-optional)
	* [Update the system](#update-the-system)
	* [Install `pip`](#install-pip)
	* [pinout](#pinout)
	* [Install dependency](#install-dependency)
* [Installing sensors](#installing-sensors)
	* [Enable the One-Wire interface](#enable-the-one-wire-interface)
	* [Setup a system service](#setup-a-system-service)
* [Managing sensors](#managing-sensors)

## Preparing a Raspberry Pi
NB: Remember to set time zone!

To prepare the Raspberry Pi for 'sensors-client' first acquire and install the Raspberry Pi OS. It is easiest obtainable through https://www.raspberrypi.com/software/. By pressing *Ctrl-Shift-X* before writing to the SD Card you will be able to later skip the steps concerning SSH, WiFi and Time Zone.

Consider the lite version of Raspberry Pi OS, as it does not install the desktop environment.

### Enable SSH
In the `boot` folder on the SD card from with the RPi run, there should be placed an empty file called `ssh` before first boot. This will enabled SSH. The file will be deleted automatically.

On the boot partition on the RPi SD run
```sh
$ touch ssh
```

### Enable WiFi
In the `boot` folder on the SD card from with the RPi run, place a file called `wpa_supplicant.conf` with SSID and key. See https://www.raspberrypi.com/documentation/computers/configuration.html#setting-up-a-headless-raspberry-pi for example. `2 letter ISO 3166-1 country code` can be found on [Wikipedia](https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes). For Denmark it is `DK`.

The file left in the `boot` folder will automatically be deleted after copied to `/etc/wpa_supplicant/wpa_supplicant.conf`.

### Set System Time
Open the config
```sh
$ sudo raspi-config
```
Pick `Localisation Options` and there after `Change Time Zone`.

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

### Install dependency
```sh
$ pip3 install w1thermsensor
$ export PATH=$PATH:/home/pi/.local/bin
```

### Install git
The easies way to install `git` is through `apt`. Compiling from source to get the newest version, should not be needed here.
```sh
$ sudo apt install git
```

## Installing sensors
Clone the repository and rename the directory
```sh
$ git clone https://github.com/ladekjaer/sensors-client-raspberry-pi-zero-w.git
$ mv sensors-client-raspberry-pi-zero-w sensors
```

### Enable the One-Wire interface
This makes it possible to read from the DS18B20 temperature sensors. Open `/boot/config.txt` and add `dtoverlay=w1-gpio` as the last line. Reboot the Raspberry Pi.

### Setup a system service
Make `sensors.service` a copy of `sensors.service.template`
```sh
$ cp sensors.service.template sensors.service
```

Update `URL` and `SENSORS_API_KEY` in `sensors.service`

Now, add `sensors.service` to the `systemd` system
```sh
$ sudo ln -s /home/pi/sensors/sensors.service /etc/systemd/system/sensors.service
$ sudo systemctl daemon-reload
$ sudo systemctl enable sensors
$ sudo systemctl start sensors
```

## Managing sensors
Use `systemctl` and `journalctl`

To see the log run
```sh
$ journalctl -u sensors
```

DigitalOcean has an easy [guide to journalctl](https://www.digitalocean.com/community/tutorials/how-to-use-journalctl-to-view-and-manipulate-systemd-logs)