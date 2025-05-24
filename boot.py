# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

#pre-loaded code above. 8 ball with gc9a01 and mpu6050 below
import settings as cfg
from machine import Timer
from accelerometer import Accelerometer
from factory import create_generator
from circular_screen import CircularScreen

# Choose a font
from fonts import vga2_16x32 as font_lrg
from fonts import vga2_8x16 as font_sml

def show(screen,generator,vector=None):
    #print(vector)
    text=generator.generate()
    screen.show(text,[font_lrg,font_sml])

def main():
    generator=create_generator(cfg.GENERATOR)
    screen=CircularScreen()
    screen.init_screen()
    mpu6050=Accelerometer(callback=lambda source,vector:show(screen,generator,vector),
                          sleep_callback=lambda source,idle_state:screen.set_idle(idle_state))
    accelerometer_timer=Timer(0)
    accelerometer_timer.init(period=250,mode=Timer.PERIODIC,
                             callback=lambda t:mpu6050.pulse())
    
    show(screen,generator)

main()


