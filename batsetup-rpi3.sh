# INSTRUCTIONS:
# 0) Modify IP address below to pi number (1, 2, 3, ...)
# 1) Place this fill in home directory (/home/pi)
# 2) chmod +x /home/pi/batsetup-rpi3.sh
# 3) Add to '/etc/rc.local' this line: '/home/pi/batsetup-rpi3.sh'

# USEFUL SOURCES:
# https://www.reddit.com/r/darknetplan/comments/68s6jp/how_to_configure_batmanadv_on_the_raspberry_pi_3/
# https://www.raspberrypi.org/documentation/linux/usage/rc-local.md

# Kill wlan0 processes
sudo pkill 'avahi'
sudo pkill 'wpa_supplicant'

# Activate batman-adv
sudo modprobe batman-adv
# Disable and configure wlan0
sudo ip link set wlan0 down
sudo ifconfig wlan0 mtu 1500
sudo iwconfig wlan0 mode ad-hoc
sudo iwconfig wlan0 essid my-mesh-network
sudo iwconfig wlan0 ap any
sudo iwconfig wlan0 channel 8
sleep 1s
sudo ip link set wlan0 up
sleep 1s
sudo batctl if add wlan0
sleep 1s
sudo ifconfig bat0 up
sleep 5s

# Use different IPv4 addresses for each device
# This is the only change necessary to the script for
# different devices. Make sure to indicate the number
# of bits used for the mask.
sudo ifconfig bat0 172.27.0.X/16
