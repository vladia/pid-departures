
import network
import config
from utime import sleep

def wifi_init():
    global wlan
    print('Connecting to WiFi Network Name:', config.SSID)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True) # power up the WiFi chip
    print('Waiting for wifi chip to power up...')
    sleep(3) # wait three seconds for the chip to power up and initialize
    wlan.connect(config.SSID, config.PASSWORD)
    print('Waiting for access point to log us in.')

def wifi_done():
    global wlan
    wlan.active(False)
    del wlan

def wifi_check():
    return wlan.isconnected()

def wifi_status():
    if wlan.isconnected():
      print('Success! We have connected to your access point!')
      print('Try to ping the device at', wlan.ifconfig()[0])
      return("Network init OK\n"+wlan.ifconfig()[0])
    else:
      print('Failure! We have not connected to your access point!  Check your config.py file for errors.')
      return("Network init FAILED.")


