## PCCAPS Smithsonian Project:

 * main.py: controls all servos, DC motors and stepper-motor via the CLI
 * app.py: a WIP Tornado web application to control the platform via HTTP

## Motors

 * DC motor: controls the tread-based platform
 * Stepper motor: controls the boom on which the camera is mounted
 * Servo 0: controls the pitch of the camera pod
 * Servo 1: controls the yaw of the camera pod

## Dependencies

 * Adafruit_MotorHAT python library (included)
 * Tornado (included)

## Tornado API

 * /tread?dir={forward, backward, left, right}&amt=SECONDS
    
    `curl 'localhost:8080/tread?dir=left&amt=1.5'`
    `curl 'localhost:8080/tread?dir=forward&amt=3'`

 * /boom?dir={up,down}&amt=STEPS
    
    `curl 'localhost:8080/boom?dir=up&amt=100'`
    `curl 'localhost:8080/boom?dir=down&amt=100'`

 * /cameraPitch={up, down}&amt=DEGREES

    `curl 'localhost:8080/cameraPitch?dir=up&amt=15'`
    `curl 'localhost:8080/cameraPitch?dir=down&amt=25'`
 
 * /cameraYaw={left, right}&amt=DEGREES

    `curl 'localhost:8080/cameraYaw?dir=left&amt=15'`
    `curl 'localhost:8080/cameraYaw?dir=right&amt=25'`
