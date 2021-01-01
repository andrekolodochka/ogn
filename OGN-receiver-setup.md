1. Set up SD card with Raspberry Pi OS Lite image.
<details>
  <summary>Configure WiFi and SSH</summary>
  1. Use instructions on [How to configure RPI for headless set up with WiFi and SSH](https://styxit.com/2017/03/14/headless-raspberry-setup.html) to configure WiFi and SSH before using SD card in Raspberry Pi. Use the following as the content of wpa_supplicat.conf file:
  
  ```ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=AU

network={
    ssid="MeMi"
    psk="<insert WiFi password here>"
    key_mgmt=WPA-PSK
    priority=1
}

network={
    ssid="Parents"
    scan_ssid=1
    psk="<insert WiFi password here>"
    key_mgmt=WPA-PSK
    priority=2
}```

2. Install SD card in RPI, boot and SSH into it. If you don’t know the IP address - try using raspberrypi.local host name (or ping it to find the IP address)
3. Configure RPI to email its IP address on boot (original instructions are on http://cagewebdev.com/raspberry-pi-sending-emails-on-boot/)
  a) Create startup_mailer.py file
  
  ```cd /home/pi
wget https://raw.githubusercontent.com/andrekolodochka/ogn/main/startup_mailer.py```

  b) Edit /etc/rc.local file and add a line to run the script on boot
  
  ```sudo vi /etc/rc.local

if [ “$_IP” ]; then
  printf “My IP address is %s\n” “$_IP”
  python /home/pi/startup_mailer.py
fi```

</details>
  
