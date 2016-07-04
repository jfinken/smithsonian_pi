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

#------------------------------------------------------------------------------
# Actually set the PWM for a given channel: 0=pitch, 1=yaw
#------------------------------------------------------------------------------
def setDegree(channel, d):
    degreePulse = servoMin
    degreePulse += int((servoMax - servoMin) / maxDegree) * d
    yawPitchCam.setPWM(channel, 0, degreePulse)

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
myStepper = mh.getStepper(50, 1)        # n steps/rev, motor port #1
myStepper.setSpeed(120)                  # RPM

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
# 3 seconds is approx. 90-degrees
#------------------------------------------------------------------------------
def left(amount):
    # LEFT for a while...
    myMotor1 = mh.getMotor(3)
    myMotor2 = mh.getMotor(4)
    
    # set the speed to start, from 0 (off) to 255 (max)
    myMotor1.setSpeed(255)
    myMotor2.setSpeed(255)

    myMotor1.run(Adafruit_MotorHAT.FORWARD)
    myMotor2.run(Adafruit_MotorHAT.BACKWARD)
    time.sleep(amount)
    turnOffMotors()

#------------------------------------------------------------------------------
# 3 seconds is approx. 90-degrees
#------------------------------------------------------------------------------
def right(amount):
    
    myMotor1 = mh.getMotor(3)
    myMotor2 = mh.getMotor(4)
    # set the speed to start, from 0 (off) to 255 (max)
    myMotor1.setSpeed(255)
    myMotor2.setSpeed(255)
    myMotor1.run(Adafruit_MotorHAT.BACKWARD)
    myMotor2.run(Adafruit_MotorHAT.FORWARD)
    time.sleep(amount)
    turnOffMotors()

#------------------------------------------------------------------------------
# Main run loop, waiting for chars from the keyboard
#------------------------------------------------------------------------------
key = '' 
#while key != 'q':
while True:

    key = raw_input("robot: ")

    #--------------------------------------------------------------------------
    # Boom control via stepper motor:
    #   y: up
    #   n: down
    # 
    # signature is: step(num_steps, direction, stepstyle (MICROSTEP for smoother)
    #--------------------------------------------------------------------------
    if key == 'y':
        myStepper.step(100, Adafruit_MotorHAT.FORWARD,  Adafruit_MotorHAT.SINGLE)
    if key == 'n':
        myStepper.step(100, Adafruit_MotorHAT.BACKWARD,  Adafruit_MotorHAT.SINGLE)

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
        # set the speed to start, from 0 (off) to 255 (max)
        myMotor1 = mh.getMotor(3)
        myMotor2 = mh.getMotor(4)
        myMotor1.setSpeed(255)
        myMotor2.setSpeed(255)
        # FORWARD for a while...
        myMotor1.run(Adafruit_MotorHAT.FORWARD) 
        myMotor2.run(Adafruit_MotorHAT.FORWARD) 
        time.sleep(3)
        turnOffMotors()

    elif key == 'a': 
        # LEFT for approx 90-deg
        left(3)
    elif key == 'q':
        # LEFT for approx 45-deg
        left(1.5)
    elif key == 'd':
        # RIGHT for approx 90-deg
        right(3)
    elif key == 'e':
        # RIGHT for approx 45-deg
        right(1.5)
    elif key == 'r':
        # left for approx 22-deg
        right(0.75)
    elif key == 't':
        # right for approx 22-deg
        left(0.75)
    elif key == '2':
        myMotor1 = mh.getMotor(3)
        myMotor2 = mh.getMotor(4)
        myMotor1.setSpeed(255)
        myMotor2.setSpeed(255)
        # FORWARD for a while...
        myMotor1.run(Adafruit_MotorHAT.FORWARD) 
        myMotor2.run(Adafruit_MotorHAT.FORWARD) 
        time.sleep(1.5)
        turnOffMotors()
    
    elif key == '3':
        # BACKWARD for a while...
        myMotor1 = mh.getMotor(3)
        myMotor2 = mh.getMotor(4)
        # set the speed to start, from 0 (off) to 255 (max)
        myMotor1.setSpeed(255)
        myMotor2.setSpeed(255)
        myMotor1.run(Adafruit_MotorHAT.BACKWARD) 
        myMotor2.run(Adafruit_MotorHAT.BACKWARD)
        time.sleep(1.5)
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

