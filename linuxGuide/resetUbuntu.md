# Reset Ubuntu

* Log in as root
````
exec sudo -i
````
* Try configuring unconfigured packages:
````
dpkg --configure -a
````
* Update the contents of the repositories
````
apt-get update
````
* Try to fix missing dependencies:
````
apt-get -f install
````
* Update your system:
````
apt-get dist-upgrade
````
* Reinstall Ubuntu desktop:
````
apt-get install --reinstall ubuntu-desktop
````
* Remove unnecessary packages:
````
apt-get autoremove
````
* Delete downloaded packages already installed:
````
apt-get clean
````
* Reboot the system to see if the issue was resolved:
````
reboot
````
