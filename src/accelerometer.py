import settings as cfg
from machine import I2C
from lib.imu import MPU6050, MPUException
import time

def noop(src,arg1=None,arg2=None):
    pass

class Accelerometer:
    '''
		The state machine goes:
		Initial:	invert_time <- None
					transitions to Inverted (always)
		Inverted:	invert_time has a value
					transitions to Triggered (on _is_inverted==False)
					transitions to Asleep (after timeout)
		Triggered:	non-inverted, and invert_time has a value:= invert_time <- None
					fire signal callback(source=this,orientation=lib.vector3d)
					transition to Initial (immediately)
		Asleep:		invert_time - now() > configured sleep
					fire signal idle_callback(source=this,True)
					transitions to Awake (on _is_inverted==False)
		Awake:		fire signal idle_callback(source=this,False)
					transition to Initial (immediately)
    '''
    INIT =0x00
    INV  =0x01
    SLEEP=0x02
    TRIG =0x04
    NOT_TRIG=INV | SLEEP
    UPRIGHT=SLEEP | TRIG
    AWAKE  =TRIG | INV
    
    def __init__(self,trig_cb=noop,idle_cb=noop,invert_cb=noop):
        self._i2c=None
        self._mpu6050=None
        self._invert_time=False
        self._callback=trig_cb
        self._idle_callback=idle_cb
        self._invert_callback=invert_cb
        self._state=Accelerometer.INIT
        self._initialise()
        
    def _initialise(self):
        print("initialise I2C")
        try:
            self._i2c = I2C(0, scl=cfg.MPU_SCL, sda=cfg.MPU_SDA, freq=cfg.I2C_CLOCK)
            self._mpu6050 = MPU6050(self._i2c)
        except MPUException as mpue:
            print(str(mpue))
            self._mpu6050 = None
            return False
        return True
        
    def _is_inverted(self,vector):
        #TODO: add a better implementation? Something with a reference vector
        return cfg.invert_predicate(vector.ixyz) #vector.ixyz[2] < cfg.INVERT_IZ
    
    def pulse(self):
        try:
            if (self._mpu6050 is None):
                if not self._initialise():
                    return
            
            vector=self._mpu6050.accel
            g_force=vector.magnitude
            #            print("ixyz " + str(vector.ixyz))
            #            print("xyz " + str(vector.xyz))
            #            print("aia " + str((vector.elevation,vector.inclination,vector.azimuth)))
            if g_force>cfg.TRIGGER_GS:
                #vector magnitude translates to G load, more or less. if > configured:
#                print("shake: " + str(vector.magnitude))
                self._shake(vector.xyz,g_force)
            inverted=self._is_inverted(vector)
            #set inversion state now. the next sequence can bail:
            if inverted:
                self._state |= Accelerometer.INV
            else:
                self._state &= Accelerometer.UPRIGHT
            #do state transitions
            if inverted:
                if self.asleep:
                    return
                if self._invert_time is None:
                    self._invert_time=time.ticks_ms()
                else:
                    #check for timeout
                    duration=time.ticks_diff(time.ticks_ms(),self._invert_time)
                    if (cfg.SLEEP_TIMEOUT_MS>0 and duration > cfg.SLEEP_TIMEOUT_MS):
                        #go to sleep
                        self._state |= Accelerometer.SLEEP
                        self._invoke_idle_cb(True)
            elif self.asleep:
                #not inverted if we get here
                self._invoke_idle_cb(False)
            elif (self._invert_time is not None):
                #not inverted and timer is on means object is righted. fire trigger:
                self._invert_time=None
                self._shake(vector.xyz,g_force)

        except MPUException as mpue:
            print(str(mpue))
            self._mpu6050=None
            
    def _shake(self,vector,g_force):
        self._state|=Accelerometer.TRIG
        try:
            self._callback(self,vector,g_force)
        except Exception as ex:
            print(str(ex))
            
    def _invoke_idle_cb(self,is_idle):
        if is_idle:
            self._state |= Accelerometer.SLEEP
        else:
            self._state &= Accelerometer.AWAKE
        try:
            self._idle_callback(self,is_idle)
        except Exception as ex:
            print(str(ex))
    
    def _set_inverted(self,is_inverted):
        if is_inverted!=self.inverted: 
            if is_inverted:
                self._state |= Accelerometer.INV
            else:
                self._state &= Accelerometer.UPRIGHT
            try:
                self._invert_callback(self,is_inverted)
            except Exception as ex:
                print(str(ex))

    @property
    def vector(self):
        return self._mpu6050.accel

    def read_and_reset_shaken(self):
        temp=self.shaken
        self._state &= Accelerometer.NOT_TRIG
        return temp

    @property
    def inverted(self):
        return (self._state & Accelerometer.INV)!=0
    
    @property
    def asleep(self):
        return (self._state & Accelerometer.SLEEP)!=0

    @property
    def shaken(self):
        return (self._state & Accelerometer.TRIG)!=0