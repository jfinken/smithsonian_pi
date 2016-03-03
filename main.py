import time
import atexit

from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
from Adafruit_MotorHAT.Adafruit_PWM_Servo_Driver import PWM

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr=0x60)

#------------------------------------------------------------------------------
# PWM control:
# Initialise the PWM device using the default address
#------------------------------------------------------------------------------
yawPitchCam = PWM(0x41, debug=False) 

servoMin = 150 # Min pulse length out of 4096
servoMax = 700 # Max pulse length out of 4096
maxDegree = 180 # Degrees your servo can rotate
degIncrease = 2 # Number of degrees to increase by each time

yawPitchCam.setPWMFreq(60) # Set PWM frequency to 60Hz

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
# UI/windowing control
# Set up curses for arrow input
#------------------------------------------------------------------------------
#scr = curses.initscr()
#curses.cbreak() 
#scr.keypad(1) 
#scr.addstr(0, 0, "Servo Volume Control")
#scr.addstr(1, 0, "UP to increase volume")
#scr.addstr(2, 0, "DOWN to decrease volume") 
#scr.addstr(3, 0, "q to quit")
#scr.refresh() 

pitchDeg = 90 # Start off at lowest volume
yawDeg = 90 # Start off at lowest volume
setDegree(0, pitchDeg) 
setDegree(1, yawDeg) 

key = '' 
#------------------------------------------------------------------------------
# Main run loop, waiting for chars from the keyboard
#------------------------------------------------------------------------------
while key != 'q':
    key = raw_input("robot: ")

    #--------------------------------------------------------------------------
    # Camera control via PWM
    # 
    # channel:
    #   0: pitch
    #   1: yaw 
    #--------------------------------------------------------------------------
    if key == 'k':
       pitchDeg += degIncrease
       # bounds check: todo: move to func 
       if pitchDeg > maxDegree:
           pitchDeg = maxDegree
       elif pitchDeg < 0:
           pitchDeg = 0

       setDegree(0, pitchDeg)
    if key == 'i':
       pitchDeg -= degIncrease
       # bounds check: todo: move to func 
       if pitchDeg > maxDegree:
           pitchDeg = maxDegree
       elif pitchDeg < 0:
           pitchDeg = 0

       setDegree(0, pitchDeg)
    
    # yaw: right 
    if key == 'l':
       yawDeg += degIncrease
       # bounds check: todo: move to func 
       if yawDeg > maxDegree:
           yawDeg = maxDegree
       elif yawDeg < 0:
           yawDeg = 0

       setDegree(1, yawDeg)
    # yaw: left 
    if key == 'j':
       yawDeg -= degIncrease
       # bounds check: todo: move to func 
       if yawDeg > maxDegree:
           yawDeg = maxDegree
       elif yawDeg < 0:
           yawDeg = 0

       setDegree(1, yawDeg)
    

    #--------------------------------------------------------------------------
    # Robot/Tread control via motors 
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
        
#curses.endwin()
