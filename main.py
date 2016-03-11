import time
import atexit

from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor
from Adafruit_MotorHAT.Adafruit_PWM_Servo_Driver import PWM

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr=0x60)

#------------------------------------------------------------------------------
# PWM control for the camera pod:
# Initialise the PWM device using the default address
#------------------------------------------------------------------------------
yawPitchCam = PWM(0x41, debug=False) 
yawPitchCam.setPWMFreq(60) # Set PWM frequency to 60Hz

servoMin = 150 # Min pulse length out of 4096
servoMax = 700 # Max pulse length out of 4096
maxDegree = 180 # Degrees your servo can rotate
degIncrease = 2 # Number of degrees to increase by each time

pitchDeg = 90 # Start off at lowest volume
yawDeg = 90 # Start off at lowest volume
setDegree(0, pitchDeg) 
setDegree(1, yawDeg) 

#------------------------------------------------------------------------------
# stepper motor config 
# TODO: tune these!
#------------------------------------------------------------------------------
myStepper = mh.getStepper(35, 1)        # 200 steps/rev, motor port #1
myStepper.setSpeed(30000)               # 30 RPM

#------------------------------------------------------------------------------
# Actually set the PWM for a given channel: 0=pitch, 1=yaw
#------------------------------------------------------------------------------
def setDegree(channel, d):
    degreePulse = servoMin
    degreePulse += int((servoMax - servoMin) / maxDegree) * d
    yawPitchCam.setPWM(channel, 0, degreePulse)


#------------------------------------------------------------------------------
# Motor control: 
#------------------------------------------------------------------------------
def turnOffMotors():
        mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
        mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
        mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
        mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

#------------------------------------------------------------------------------
# Assert yaw-pitch is not out of bounds
#------------------------------------------------------------------------------
def checkYawPitch(deg):
    if deg > maxDegree:
        deg = maxDegree
    elif deg < 0:
        deg = 0
    return deg

#------------------------------------------------------------------------------
# Main run loop, waiting for chars from the keyboard
#------------------------------------------------------------------------------
key = '' 
while key != 'q':

    key = raw_input("robot: ")

    #--------------------------------------------------------------------------
    # Boom control via stepper motor:
    #   y: up
    #   n: down
    # 
    # TODO: completely untested on the pi...
    #--------------------------------------------------------------------------
    if key == 'y':
        myStepper.step(50, Adafruit_MotorHAT.FORWARD,  Adafruit_MotorHAT.MICROSTEP)
    if key == 'n':
        myStepper.step(50, Adafruit_MotorHAT.BACKWARD,  Adafruit_MotorHAT.MICROSTEP)

    #--------------------------------------------------------------------------
    # Camera servo control via PWM
    # 
    # channel:
    #   0: pitch
    #   1: yaw 
    #--------------------------------------------------------------------------
    if key == 'k':
       pitchDeg += degIncrease
       pitchDeg = checkYawPitch(pitchDeg)
       setDegree(0, pitchDeg)

    if key == 'i':
       pitchDeg -= degIncrease
       pitchDeg = checkYawPitch(pitchDeg)
       setDegree(0, pitchDeg)
    
    # yaw: right 
    if key == 'l':
       yawDeg += degIncrease
       yawDeg = checkYawPitch(yawDeg)
       setDegree(1, yawDeg)
    # yaw: left 
    if key == 'j':
       yawDeg -= degIncrease
       yawDeg = checkYawPitch(yawDeg)
       setDegree(1, yawDeg)

    #--------------------------------------------------------------------------
    # Robot/Tread control via DC motors 
    #--------------------------------------------------------------------------
    if key == 'w':
        # FORWARD for a while...
        myMotor1 = mh.getMotor(3)
        myMotor2 = mh.getMotor(4)
        myMotor1.setSpeed(255)
        myMotor2.setSpeed(255)
        # set the speed to start, from 0 (off) to 255 (max)
        myMotor1.run(Adafruit_MotorHAT.FORWARD) 
        myMotor2.run(Adafruit_MotorHAT.FORWARD) 
        time.sleep(3)
        turnOffMotors()

    elif key == 'a': 
        # LEFT for a while...
        myMotor1 = mh.getMotor(3)
        myMotor2 = mh.getMotor(4)
        
        # set the speed to start, from 0 (off) to 255 (max)
        myMotor1.setSpeed(255)
        myMotor2.setSpeed(255)

        myMotor1.run(Adafruit_MotorHAT.FORWARD)
        myMotor2.run(Adafruit_MotorHAT.BACKWARD)
        time.sleep(3)
        turnOffMotors()

    elif key == 'd':
        # RIGHT for a while...
        myMotor1 = mh.getMotor(3)
        myMotor2 = mh.getMotor(4)
        # set the speed to start, from 0 (off) to 255 (max)
        myMotor1.setSpeed(255)
        myMotor2.setSpeed(255)
        myMotor1.run(Adafruit_MotorHAT.BACKWARD)
        myMotor2.run(Adafruit_MotorHAT.FORWARD)
        time.sleep(3)
        turnOffMotors()

    elif key == 's':
        # BACKWARD for a while...
        myMotor1 = mh.getMotor(3)
        myMotor2 = mh.getMotor(4)
        # set the speed to start, from 0 (off) to 255 (max)
        myMotor1.setSpeed(255)
        myMotor2.setSpeed(255)
        myMotor1.run(Adafruit_MotorHAT.BACKWARD) 
        myMotor2.run(Adafruit_MotorHAT.BACKWARD)
        time.sleep(3)
        turnOffMotors()
