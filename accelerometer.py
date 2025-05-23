import settings as cfg
from machine import Pin, I2C
from imu import MPU6050, MPUException

class Accelerometer:
    
    def __init__(self,callback):
        self.i2c=None
        self.mpu6050=None
        self.inverted=False
        #self.shaken=False
        self.callback=callback
        self.initialise()
        
    def initialise(self):
        print("initialise I2C")
        try:
            self.i2c = I2C(0, scl=cfg.MPU_SCL, sda=cfg.MPU_SDA, freq=cfg.I2C_CLOCK)
            self.mpu6050 = MPU6050(self.i2c)
        except MPUException as mpue:
            print(str(mpue))
            self.mpu6050 = None
            return False
        return True
        
    def _is_inverted(self,vector):
        #TODO: add a better implementation with a reference vector
        return vector.z > 0
            
    def pulse(self):
        try:
            if (self.mpu6050 is None):
                if not self.initialise():
                    return
            
            vector=self.mpu6050.accel
            #if the G load is > configured:
            if vector.magnitude>cfg.TRIGGER_GS:
#                print("shake: " + str(vector.magnitude))
#                self.shaken=True
                self.callback(self,vector)
            #otherwise if flipped upside down, latch inversion on:
            if self._is_inverted(vector):
                self.inverted=True
            #if inversion latch on and not inverted, trigger a shake:
            elif (self.inverted):
                self.inverted=False
#                self.shaken=True
                self.callback(self,vector)

        except MPUException as mpue:
            print(str(mpue))
#            del self.mpu6050
            self.mpu6050=None

    def shaken(self):
        return self.shaken
        