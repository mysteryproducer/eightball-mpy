# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

#pre-loaded code above. 8 ball with gc9a01 and mpu6050 below
# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

import random, time, math
from machine import Pin, SPI, I2C
import gc9a01py as gc9a01
from imu import MPU6050, MPUException
from gen import create_generator
#import bno08x_i2c as bno08x

# Choose a font
from fonts import vga1_16x32 as font
#from fonts import vga2_bold_16x32 as font
#from images import blank as triangle

#constants
blue=gc9a01.color565(47,32,245)
#MPU6050 uses an I2C connection; need clock (SCL) and data (SDA)
MPU_SCL=Pin(13)
MPU_SDA=Pin(12)
#GC9A01 screen uses SPI interface; more pins needed:
SCR_SCK=Pin(1, Pin.OUT) #clock
SCR_MOSI=Pin(2, Pin.OUT) #data
SCR_DC=Pin(3, Pin.OUT) #
SCR_CS=Pin(4, Pin.OUT) # channel select
SCR_RESET=Pin(5, Pin.OUT)

#global state
tft=None
mpu6050=None
screen_pow=Pin(6, Pin.OUT)
invert_latch=False
#base-level comms interfaces
i2c=None
spi=None

generator=create_generator("dsm5")
#options=["Yes","No","A school","Unlikely!","Fluxus says"]
def genText():
    return generator.generate()
#    try:
#        index=math.floor(random.random()*len(options))
#        return options[index]
#    except:
#        return options[0]


def show():
    tft.fill(blue)
    tft.text(font,genText(),
        100,
        100,
        gc9a01.WHITE,blue
    )

def init_MPU():
    global mpu6050, i2c
    print("initialise I2C")
    i2c = I2C(0, scl=MPU_SCL, sda=MPU_SDA, freq=100000)
    mpu6050 = MPU6050(i2c)
#    bno = bno08x.BNO08X_I2C(i2c, address=i2c.scan()[0])
#    bno.enable_feature(bno08x.BNO_REPORT_SHAKE_DETECTOR)
#    bno.enable_feature(bno08x.BNO_REPORT_GRAVITY)
    
def init_screen():
    global tft, spi
    screen_pow.value(1)
    print("initialise SPI")
    spi = SPI(1, baudrate=10000000, sck=SCR_SCK, mosi=SCR_MOSI)
#    print(spi)
    tft = gc9a01.GC9A01(
        spi,
        dc=SCR_DC,
        cs=SCR_CS,
        reset=SCR_RESET,
        backlight=None,#Pin(7, Pin.OUT),
        rotation=0)
    tft.fill(blue)
#TODO: print start message: power level?

#    col_max = tft.width - font.WIDTH*6
#    row_max = tft.height - font.HEIGHT
#    tft.text(font,"YES",
#             100,
#             100,
#             gc9a01.WHITE,blue
#    )
#    tft.blit_buffer(triangle.BITMAP,0,0,240,240)

def loop():
    global invert_latch

    shaken=False
    time.sleep(0.5)
    accel=mpu6050.accel
#    print(str(accel.x)+" ,"+str(accel.y)+", "+str(accel.z)+" -> " + str(accel.magnitude))
#    print(str(accel.z))
# MPU6050 outputs in Gs, so magnitude will be ~ 1 when still.
# Shaking will record a higher G load
    if accel.magnitude>1.3:
        print("shake: " + str(accel.magnitude))
        shaken=True
    if accel.z > 0:
        invert_latch=True
    elif (invert_latch):
        print("invert")
        invert_latch=False
        shaken=True
    if shaken:
        show()

def main():
    global i2c
    init_MPU()
    init_screen()  
    show()
    
    should_loop=True
    while should_loop:
        try:
            loop()
        except MPUException as mpue:
            print(str(mpue))
            del i2c
            init_MPU()
        except Exception as ex:
            print(str(ex))
            should_loop=False
    screen_pow.value(0)

main()




