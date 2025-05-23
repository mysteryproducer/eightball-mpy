# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

#pre-loaded code above. 8 ball with gc9a01 and mpu6050 below
import random, time, math
import settings as cfg
from machine import Pin, SPI, I2C, Timer
from accelerometer import Accelerometer
from imu import MPU6050, MPUException
from factory import create_generator
from circular_screen import CircularScreen

# Choose a font
from fonts import vga2_16x32 as font_lrg
from fonts import vga2_8x16 as font_sml

def show(screen,generator,vector=None):
    print(vector)
    text=generator.generate()
    screen.show(text,[font_lrg,font_sml])

def main():
    mpu6050=Accelerometer(lambda source,vector:show(screen,generator,vector))
    generator=create_generator(cfg.GENERATOR)
    accelerometer_timer=Timer(0)
    accelerometer_timer.init(period=250,mode=Timer.PERIODIC,
                             callback=lambda t:mpu6050.pulse())
    
    screen=CircularScreen()
    screen.init_screen()
    show(screen,generator)

main()


