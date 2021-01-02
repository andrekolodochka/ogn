These instructions are for headless installation (that's without a need for keyboard and monitor connected to Raspberry Pi). Well, at least for the most part, you still have to connect to RPI to configure WiFi and enable SSH. I created a custom RPI image which has those already pre-configured for my home wifi so I can skip the step #1 below.

Set up SD card with [Raspberry Pi OS Lite image](https://www.raspberrypi.org/software/operating-systems/#raspberry-pi-os-32-bit).
  

<details>
  <summary>1. Configure WiFi, SSH, timezone, hostname</summary>
  Skip this step if using pre-confgured RPI image 
  
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
}
```

2. Install SD card in RPI, boot and SSH into it. If you don’t know the IP address - try using raspberrypi.local host name (or ping it to find the IP address)
3. Configure RPI to email its IP address on boot (original instructions are on http://cagewebdev.com/raspberry-pi-sending-emails-on-boot/)
  a) Create startup_mailer.py file
  
  ```cd /home/pi
wget https://raw.githubusercontent.com/andrekolodochka/ogn/main/startup_mailer.py
```

  b) Edit /etc/rc.local file and add a line to run the script on boot
  
  ```sudo vi /etc/rc.local

if [ “$_IP” ]; then
  printf “My IP address is %s\n” “$_IP”
  python /home/pi/startup_mailer.py
fi
```
4. Set Raspberry Pi settings through *raspi-config*

```
sudo raspi-config
```

a) *1. System options → S4 Hostname*: set preferred hostname, such as YSRI-OGN-receiver

b) *5. Localization options → L2 Timezone*: set to Australia/Sydney
</details>

<details>
  <summary>2. Update existing and install new required packages</summary>
    
```
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y build-essential ntp ntpdate libjpeg-dev libconfig-dev fftw3-dev procserv lynx telnet rtl-sdr make cmake aptitude libjpeg8
```

</details>

<details>
  <summary>3. Download rtl-dsr software and extract</summary>
  
```
sudo mkdir /opt/rtlsdr && cd /opt/rtlsdr && sudo wget http://download.glidernet.org/arm/rtlsdr-ogn-bin-ARM-latest.tgz && sudo tar -xzvf rtlsdr-ogn-bin-ARM-latest.tgz
cd rtlsdr-ogn
```
</details>
  
<details>
  <summary>4. Follow instructions in INSTALL file</summary>
  
```
source setup-rpi.sh
source getEGM.sh
source install-service.sh
```
</details>
  
<details>
  <summary>5. Download configuration file for YSRI</summary>
  Obviously this step is specific to Richmond RAAF airbase, you'll need to figure out your airfield's settings
  
  ```
  wget -O /opt/rtldsr/rtlsdr-ogn/YSRI.conf https://raw.githubusercontent.com/andrekolodochka/ogn/main/YSRI.conf
  ```
  
  </details>
  
<details>
  <summary>6. Download rtlsdr-ogn.conf file into /etc directory and overwrite the existing file</summary>
  Again, this step is specific to my set up, the name and location of your configuration file rtl-sdr-ogn.conf refers to is likely to be different.
  
  ```
  sudo wget -O /etc/rtldsr-ogn.conf https://raw.githubusercontent.com/andrekolodochka/ogn/main/rtlsdr-ogn.conf
  ```
  
</details>
  
<details>
  <summary>7. Plug in the dongle and start the service</summary>
  
  ```
  sudo service rtlsdr-ogn start 
  ```
  
</details> 
<details>
  <summary>Test and monitor/summary>
  
  1. Should see fair bit of activity on port 50001 (may need to wait a few mins after the start)
  
  ```
  telnet localhost 50000
  telnet localhost 50001
  ```
  2. Open http://<receiver IP address>:8081 and http://<receiver IP address>:8080
  3. Go to [Glider RADAR](https://www.gliderradar.com/center/-33.59749,150.78493/zoom/15/time/15) and check whether the receiver is shown. Go to [Onglide Range](https://ognrange.glidernet.org/?#,max,all,-33.59206_150.81118,10,#000000ff:#000000ff,circles;) and check whether YSRI receiver is online.
