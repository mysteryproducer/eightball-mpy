# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

#pre-loaded code above. 8 ball with gc9a01 and mpu6050 below
import random, time, math
import settings as cfg
from machine import Pin, SPI, I2C
from imu import MPU6050, MPUException
from gen import create_generator
from circular_screen import CircularScreen
#import bno08x_i2c as bno08x

# Choose a font
from fonts import vga1_16x32 as font_lrg
from fonts import vga1_8x16 as font_sml

#global state
mpu6050=None
invert_latch=False
screen=None
generator=create_generator(cfg.GENERATOR)
#base-level comms interfaces
i2c=None

def show():
    text=generator.generate()
    screen.show(text,[font_lrg])

def init_MPU():
    global mpu6050, i2c
    print("initialise I2C")
    i2c = I2C(0, scl=cfg.MPU_SCL, sda=cfg.MPU_SDA, freq=cfg.I2C_CLOCK)
    mpu6050 = MPU6050(i2c)
#    bno = bno08x.BNO08X_I2C(i2c, address=i2c.scan()[0])
#    bno.enable_feature(bno08x.BNO_REPORT_SHAKE_DETECTOR)
#    bno.enable_feature(bno08x.BNO_REPORT_GRAVITY)


def loop():
    global invert_latch

    shaken=False
    time.sleep(0.5)
    accel=mpu6050.accel
#    print(str(accel.x)+" ,"+str(accel.y)+", "+str(accel.z)+" -> " + str(accel.magnitude))
#    print(str(accel.z))
    if accel.magnitude>cfg.TRIGGER_GS:
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
    global screen
    init_MPU()
    
    screen=CircularScreen()
    screen.init_screen()
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
    screen.stop()

main()
