
import config
import machine
import webrepl
import gc

from golemiofunc import *
from displayfunc import *
from wififunc import *
from timefunc import *

class state:
    NONE = 1
    NETWORK_PREINIT = 2
    NETWORK_INIT = 3
    NETWORK_REINIT = 8    
    TIME_SYNC = 4
    TIME_RESYNC = 5
    APP_INIT = 6
    APP_RDY = 7

if __name__=='__main__':

    gc.enable()
    sleep_pin = machine.Pin(config.PIR_PIN, Pin.IN, Pin.PULL_UP)
    display_init()

    """
    LCD.fill(LCD.WHITE)
    LCD.show_up()

    while True:
        if sleep_pin():
            LCD.bl_ctrl(100)
        else:
            LCD.bl_ctrl(0)
        time.sleep_ms(10)
    """

#    time.sleep(2)
    """
    print("Before bytearray creation", gc.mem_free())
    #gc.collect    
    LCD.bl_ctrl(70)
    LCD.fill(LCD.BLACK)
  
    printstatus("Network Init...")

    retval = wifi_init()
    """


    """
    retval = wifi_init()

    while not wifi_check():
       time.sleep_ms(100)



    printstatus(wifi_status())
    """

#    printstatus("Network Init..→.")
#    while True:
#        time.sleep(3)

    webrepl.start(password=config.WEBREPL_PASSWORD)

    rtc = machine.RTC()
    st = state.NETWORK_PREINIT
    prev_backlight=1
    curr_backlight=1    
    start_ts = get_ts()
    lastok_ts = start_ts
    while True:

        current_ts = get_ts()

        if (st == state.NETWORK_PREINIT):
            printstatus("Network Init...")

            retval = wifi_init()

            st = state.NETWORK_INIT

        elif (st == state.NETWORK_INIT):
            if wifi_check():
               printstatus(wifi_status())
               st = state.TIME_SYNC
               start_ts =  get_ts()
            if current_ts > (start_ts + 20):
               st = state.NETWORK_REINIT

        elif (st == state.NETWORK_REINIT):
            wifi_done()
            st = state.NETWORK_PREINIT

        elif (st == state.TIME_SYNC) or (st == state.TIME_RESYNC) :
            retval, text = ntp_sync()
            if retval == True:
                if (st == state.TIME_RESYNC):
                    st = state.APP_RDY
                else:
                    printstatus("Time OK")
                    st = state.APP_INIT
                lastntp_ts = get_ts()
            else:
                if (st == state.TIME_RESYNC):
                    st = state.APP_RDY
                else:
                    printstatus(text)
                    time.sleep(3)

        elif (st == state.APP_INIT):
            next_ts = 0
            start_ts = get_ts()
            st = state.APP_RDY

        elif (st == state.APP_RDY):
            if not wifi_check():            
                printstatus("No Connection...")
                time.sleep(3)
                st = state.NETWORK_REINIT
                continue

            if (current_ts > (lastntp_ts + 3600)):
                st = state.TIME_RESYNC
                continue

            if (current_ts > next_ts) and not ((config.BACKLIGHT_MIN == 0) and (curr_backlight == 0)):
                retval, data = golemio_get_data()
                print(retval)

                if retval:
                    printdata(data, rtc)
                    lastok_ts = current_ts
                else:
                    if (current_ts > (lastok_ts + 60)):
                        printstatus(data)
                        time.sleep(3)

                next_ts = current_ts + config.DISPLAY_REFRESH

        if (current_ts > (start_ts + 60)) and config.PIR_ENABLED:
            if sleep_pin():
                curr_backlight = 1
                if (prev_backlight != curr_backlight):
                    print("backlight on")
                    display_setbl(config.BACKLIGHT_MAX)
            else:
                curr_backlight = 0
                if (prev_backlight != curr_backlight):
                    print("backlight off")
                    display_setbl(config.BACKLIGHT_MIN)
                    if config.BACKLIGHT_MIN == 0:
                        printstatus("Wake up...")
            prev_backlight = curr_backlight

        time.sleep_ms(100)
