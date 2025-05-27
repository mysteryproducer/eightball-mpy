# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

#pre-loaded code above. 8 ball with gc9a01 and mpu6050 below
import settings as cfg
from time import sleep
from machine import Timer, Pin
from accelerometer import Accelerometer
from factory import create_generator
from circular_screen import CircularScreen

# Choose a font
from fonts import vga2_16x32 as font_lrg
from fonts import vga2_8x16 as font_sml

def show(screen,generator,vector=None,g_load=None):
    text=generator.generate()
    screen.show(text,[font_lrg,font_sml])

def main():
    generator=create_generator(cfg.GENERATOR)
    screen=CircularScreen()
    screen.init_screen()
    mpu6050=Accelerometer(trig_cb=lambda src,v,gs:show(screen,generator,v,gs),
                          idle_cb=lambda src,idle:screen.set_idle(idle),
                          invert_cb=lambda src,inv:print(inv))
    accelerometer_timer=Timer(0)
    accelerometer_timer.init(period=250,mode=Timer.PERIODIC,
                             callback=lambda t:mpu6050.pulse())
    
    show(screen,generator)
    return (generator,screen,mpu6050,accelerometer_timer)

all_state=main()

#test_timer=Timer(1)
#test_timer.init(period=2000,mode=Timer.PERIODIC,
#                             callback=lambda t:print(all_state[2].vector.ixyz))
