
import machine
import config
import ntptime
import utime

def get_ts():
    return utime.mktime(utime.localtime())

def ntp_sync():
    global rtc
    try:            
        ntptime.settime()

        if 'rtc' in globals():
           del rtc
        rtc = machine.RTC()
        utc_shift = config.UTC_OFFSET

        tm = utime.localtime(utime.mktime(utime.localtime()) + utc_shift*3600)                
        tm = tm[0:3] + (0,) + tm[3:6] + (0,)
        rtc.datetime(tm)
        lastntp_ts = utime.mktime(utime.localtime())                
        print(rtc.datetime())

        return True, None

    except Exception as error:
        print("An exception occurred:", error, type(error).__name__)
        return False, str(error) + "\n" + type(error).__name__

