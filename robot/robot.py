import time
import atexit
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor
from Adafruit_MotorHAT.Adafruit_PWM_Servo_Driver import PWM

class Robot():
    def __init__(self):
        self.Name = 'Sparky'
        atexit.register(self.turnOffMotors)
        # create a default object, no changes to I2C address or frequency
        self.mh = Adafruit_MotorHAT(addr=0x60)

        #------------------------------------------------------------------------------
        # PWM control for the camera pod:
        # Initialise the PWM device using the default address
        #------------------------------------------------------------------------------
        #self.yawPitchCam = PWM(0x41, debug=False) 
        #self.yawPitchCam.setPWMFreq(60) # Set PWM frequency to 60Hz
        
        #------------------------------------------------------------------------------
        # stepper motor config 
        #------------------------------------------------------------------------------
        #myStepper = mh.getStepper(50, 1)        # n steps/rev, motor port #1
        #myStepper.setSpeed(120)                  # RPM

        self.servoMin = 150     # Min pulse length out of 4096
        self.servoMax = 700     # Max pulse length out of 4096
        self.maxDegree = 180    # Degrees your servo can rotate
        self.degIncrease = 2    # Number of degrees to increase by each time
        self.pitchDeg = 90      # Start off at lowest volume
        self.yawDeg = 90        # Start off at lowest volume
        
        self.setDegree(0, self.pitchDeg) 
        self.setDegree(1, self.yawDeg) 

    #------------------------------------------------------------------------------
    # Assert yaw-pitch is not out of bounds
    #------------------------------------------------------------------------------
    def checkYawPitch(self, deg):
        if deg > self.maxDegree:
            deg = self.maxDegree
        elif deg < 0:
            deg = 0
        return deg

    #--------------------------------------------------------------------------
    # Boom control via stepper motor:
    #   y: up
    #   n: down
    # 
    # signature is: step(num_steps, direction, stepstyle (MICROSTEP for smoother)
    #--------------------------------------------------------------------------
    def BoomUp(self):
        return
        myStepper.step(100, Adafruit_MotorHAT.FORWARD,  Adafruit_MotorHAT.SINGLE)
    def BoomDown(self):
        return
        myStepper.step(100, Adafruit_MotorHAT.BACKWARD,  Adafruit_MotorHAT.SINGLE)

    #------------------------------------------------------------------------------
    # Camera servo control via PWM
    # 
    # channel:
    #   0: pitch
    #   1: yaw 
    #------------------------------------------------------------------------------
    def CameraPitchUp(self):
        self.pitchDeg += self.degIncrease
        self.pitchDeg = self.checkYawPitch(self.pitchDeg)
        self.setDegree(0, self.pitchDeg)

    def CameraPitchDown(self):
        self.pitchDeg -= self.degIncrease
        self.pitchDeg = self.checkYawPitch(self.pitchDeg)
        self.setDegree(1, deg)

    def CameraYawLeft(self):
        self.yawDeg += self.degIncrease
        self.yawDeg = self.checkYawPitch(self.yawDeg)
        self.setDegree(1, self.yawDeg)

    def CameraYawRight(self):
        self.yawDeg -= self.degIncrease
        self.yawDeg = self.checkYawPitch(self.yawDeg)
        self.setDegree(1, self.yawDeg)

    def setDegree(self, channel, d):
        return
        self.degreePulse = self.servoMin
        self.degreePulse += int((self.servoMax - self.servoMin) / self.maxDegree) * d
        self.yawPitchCam.setPWM(channel, 0, degreePulse)

    #--------------------------------------------------------------------------
    # Robot/Tread control via DC motors 
    #--------------------------------------------------------------------------
    def TreadForward(self):
        # set the speed to start, from 0 (off) to 255 (max)
        myMotor1 = self.mh.getMotor(3)
        myMotor2 = self.mh.getMotor(4)
        myMotor1.setSpeed(255)
        myMotor2.setSpeed(255)
        # FORWARD for a while...
        myMotor1.run(Adafruit_MotorHAT.FORWARD) 
        myMotor2.run(Adafruit_MotorHAT.FORWARD) 
        time.sleep(3)
        self.turnOffMotors()

    def TreadBackward(self):
        # set the speed to start, from 0 (off) to 255 (max)
        myMotor1 = self.mh.getMotor(3)
        myMotor2 = self.mh.getMotor(4)
        myMotor1.setSpeed(255)
        myMotor2.setSpeed(255)
        # BACKWARD for a while...
        myMotor1.run(Adafruit_MotorHAT.BACKWARD) 
        myMotor2.run(Adafruit_MotorHAT.BACKWARD)
        time.sleep(3)
        self.turnOffMotors()

    def TreadLeft(self, amount):
        # set the speed to start, from 0 (off) to 255 (max)
        '''
        myMotor1 = self.mh.getMotor(3)
        myMotor2 = self.mh.getMotor(4)
        myMotor1.setSpeed(255)
        myMotor2.setSpeed(255)

        # LEFT for: 3 sec is approx 90-deg
        myMotor1.run(Adafruit_MotorHAT.FORWARD)
        myMotor2.run(Adafruit_MotorHAT.BACKWARD)
        '''
        print("robot - treadleft for {}".format(amount))
        time.sleep(amount)
        self.turnOffMotors()
   
    def TreadRight(self, amount):
        # set the speed to start, from 0 (off) to 255 (max)
        myMotor1 = self.mh.getMotor(3)
        myMotor2 = self.mh.getMotor(4)
        myMotor1.setSpeed(255)
        myMotor2.setSpeed(255)
        # RIGHT for: 3 sec is approx 90-deg
        myMotor1.run(Adafruit_MotorHAT.BACKWARD)
        myMotor2.run(Adafruit_MotorHAT.FORWARD)
        print("robot - treadRight for {}".format(amount))
        time.sleep(amount)
        self.turnOffMotors()

    def turnOffMotors(self):
        self.mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
        self.mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
        self.mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
        self.mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

