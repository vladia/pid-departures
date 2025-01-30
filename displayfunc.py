
from lcd_3inch5 import *
import config
import microfont

def display_init():
    global font, LCD
    font = microfont.MicroFont("font.mfnt",cache_index=True)
    LCD = LCD_3inch5(rotate=config.DISPLAY_ROTATION)
    LCD.bl_ctrl(config.BACKLIGHT_MAX)
    LCD.fill(LCD.BLACK)
    LCD.show_up()

def display_setbl(bl):
    LCD.bl_ctrl(bl)

class textalign:
    LEFT = 0
    MIDDLE = 1
    RIGHT = 2

def printdisp(x, y, text, align=textalign.LEFT, color=LCD_3inch5.WHITE):
    x = int(x)
    y = int(y)
    angle = 0
    if align == textalign.LEFT:
         font.write(text, LCD, framebuf.RGB565, LCD.width, LCD.height, x, y, color, rot=angle, x_spacing=0, y_spacing=0)
    elif align == textalign.MIDDLE:
         width, height = font.write(text, LCD, framebuf.RGB565, LCD.width, LCD.height, x, y, color, rot=angle, x_spacing=0, y_spacing=0, draw=0)
         font.write(text, LCD, framebuf.RGB565, LCD.width, LCD.height, x-int(width/2), y-int(height/2), color, rot=angle, x_spacing=0, y_spacing=0)        
    elif align == textalign.RIGHT:
         width, height = font.write(text, LCD, framebuf.RGB565, LCD.width, LCD.height, x, y, color, rot=angle, x_spacing=0, y_spacing=0, draw=0)
         font.write(text, LCD, framebuf.RGB565, LCD.width, LCD.height, x-width, y, color, rot=angle, x_spacing=0, y_spacing=0)        

def printstatus(status):
    LCD.fill(LCD.BLACK)    
    printdisp(LCD.width/2,LCD.height/2,status,align=textalign.MIDDLE)
    LCD.show_up()

weekdays = ["pondělí","úterý","středa","čtvrtek","pátek","sobota","neděle"]

def printdata(data, rtc):
    LCD.fill(LCD.BLACK)
    i=0;

#    for stop in data["stops"]:
    for stop in config.STOPS:
        if "descr" in stop:
            descr = stop["descr"]
        else:
            for remote_stop in data["stops"]:
               if remote_stop["stop_id"] == stop["id"]:
                  descr = remote_stop["stop_name"]

        printdisp(0,i, descr)
        printdisp(LCD.width,i,"Min.", align=textalign.RIGHT)
        i = i + font.height
        LCD.rect(0,i,LCD.width,2,LCD.WHITE)
        i = i + 2
        for departure in data["departures"]:
            if stop["id"] == departure["stop"]["id"]:
               minutes = departure["departure_timestamp"]["minutes"]
               if (minutes == "<1") or (int(minutes) <= stop["time2go"]):
                   color=LCD.RED
               else:
                   color=LCD.WHITE
               printdisp(0,i,departure["route"]["short_name"], color=color)
               printdisp(50,i,departure["trip"]["headsign"], color=color)
               printdisp(LCD.width,i, minutes, align=textalign.RIGHT, color=color)
               i = i + font.height
#              LCD.rect(0,i,LCD.width,2,LCD.WHITE)
        i = i + 15

    LCD.rect(0,LCD.height-font.height-2,LCD.width,2,LCD.WHITE)
    year, month, day, weekday, hours, minutes, seconds, aa = rtc.datetime()
    printdisp(0, LCD.height-font.height, "%s %02d.%02d.%d" % (weekdays[weekday], day, month, year))
    printdisp(LCD.width, LCD.height-font.height, "%02d:%02d" % (hours,minutes), align=textalign.RIGHT)
    LCD.show_up()

