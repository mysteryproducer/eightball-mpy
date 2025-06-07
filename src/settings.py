from machine import Pin

#MPU6050 uses an I2C connection; need clock (SCL) and data (SDA)
MPU_SCL=Pin(13)
MPU_SDA=Pin(12)
I2C_CLOCK=100000
#GC9A01 screen uses SPI interface; more pins needed:
SCR_SCK=Pin(1, Pin.OUT) #clock
SCR_MOSI=Pin(2, Pin.OUT) #data
SCR_DC=Pin(3, Pin.OUT) #
SCR_CS=Pin(4, Pin.OUT) # channel select
SCR_RESET=Pin(5, Pin.OUT)
SPI_CLOCK=40000000
# This is the switch pin for the screen.
SCR_POW=6

GENERATOR="dsm5"
# MPU6050 outputs in Gs, so magnitude will be ~ 1 when still.
# Shaking will record a higher G load
TRIGGER_GS=1.3
SLEEP_TIMEOUT_MS=30000
TRIGGER_COOLDOWN=1000

invert_predicate=lambda v: v[2] < -12000