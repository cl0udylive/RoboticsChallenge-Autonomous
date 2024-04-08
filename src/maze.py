#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code
brain_inertial = Inertial()
left_drive_smart = Motor(Ports.PORT7, 1.0, False)
right_drive_smart = Motor(Ports.PORT12, 1.0, True)

drivetrain = SmartDrive(left_drive_smart, right_drive_smart, brain_inertial, 200)
distance_left = Distance(Ports.PORT2)
distance_frontL = Distance(Ports.PORT3)
touchled_8 = Touchled(Ports.PORT8)
distance_right = Distance(Ports.PORT10)
distance_frontR = Distance(Ports.PORT4)



# Make random actually random
def setRandomSeedUsingAccel():
    wait(100, MSEC)
    xaxis = brain_inertial.acceleration(XAXIS) * 1000
    yaxis = brain_inertial.acceleration(YAXIS) * 1000
    zaxis = brain_inertial.acceleration(ZAXIS) * 1000
    urandom.seed(int(xaxis + yaxis + zaxis))
    
# Set random seed 
setRandomSeedUsingAccel()

vexcode_initial_drivetrain_calibration_completed = False
def calibrate_drivetrain():
    # Calibrate the Drivetrain Inertial
    global vexcode_initial_drivetrain_calibration_completed
    sleep(200, MSEC)
    brain.screen.print("Calibrating")
    brain.screen.next_row()
    brain.screen.print("Inertial")
    brain_inertial.calibrate()
    while brain_inertial.is_calibrating():
        sleep(25, MSEC)
    vexcode_initial_drivetrain_calibration_completed = True
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)

#endregion VEXcode Generated Robot Configuration

# ------------------------------------------
# 
# 	Project:      VEXcode Project
# 	Author:       VEX
# 	Created:
# 	Description:  VEXcode IQ Python Project
# 
# ------------------------------------------

# Library imports
from vex import *

# Begin project code



# Robot configuration code
brain_inertial = Inertial()
left_drive_smart = Motor(Ports.PORT7, 1.0, True)
right_drive_smart = Motor(Ports.PORT12, 1.0, False)

drivetrain = SmartDrive(left_drive_smart, right_drive_smart, brain_inertial, 200)
controller = Controller()
distance_left = Distance(Ports.PORT2)
distance_right = Distance(Ports.PORT10)
distance_frontL = Distance(Ports.PORT3)
distance_frontR = Distance(Ports.PORT4)
touchLed = Touchled(Ports.PORT8)

# Calibrate Robot CPU
brain.screen.set_font(FontType.MONO15)
brain.screen.print("Calibrating")
brain.screen.next_row()
brain.screen.print("Remain Still")
brain.screen.next_row()
brain.screen.print("Approx. Time:")
brain.screen.next_row()
brain.screen.print("5 Seconds")
brain_inertial.calibrate()
brain_inertial.set_heading(0.0, DEGREES)
brain_inertial.set_rotation(0.0, DEGREES)
touchLed.set_brightness(100)
currentHeading = brain_inertial.heading()
wait(5, SECONDS)

brain.screen.clear_screen()
brain.screen.set_cursor(1, 1)
brain.screen.print("Complete!")
wait(2, SECONDS)

brain.screen.clear_screen()
brain.screen.set_cursor(1, 1)



# Initialize and Calibrate Robot Sensors and Devices
drivetrain.set_stopping(HOLD)
drivetrain.set_heading(0.0, DEGREES)
drivetrain.set_rotation(0.0, DEGREES)



brain.screen.clear_screen()
brain.screen.set_cursor(1, 1)

#distance Threshold tells the sensors how close an object should be to be considered an obstacle 
#Inches 
distanceThreshold = 9

drivetrain.set_drive_velocity(30, PERCENT)
drivetrain.set_turn_velocity(33, PERCENT)


#Use this funciton for turning, every other on is too slow for some reason
def turnTo(angle, direction = ""):
        if direction == "L":
            angle = 360 - angle
        drivetrain.set_heading(0, DEGREES)
        drivetrain.turn_to_heading(angle, DEGREES, wait=True)

def align():
    touchLed.set_color(Color.GREEN)
    SENSOR_SEPARATION = 101.6 # millimeters
    deltaFrontDistance = (distance_frontL.object_distance(MM) - distance_frontR.object_distance(MM)) / SENSOR_SEPARATION
    turnRadius = round(math.degrees(math.atan(deltaFrontDistance)))
    
    # Example:
    if turnRadius < 0:
        drivetrain.turn_for(RIGHT, abs(turnRadius), DEGREES, wait=True)
        print("turning right for ", abs(turnRadius), " degrees")
        brain.screen.set_cursor(3,3)
        brain.screen.print(turnRadius)
        turnTo(turnRadius)
    else:
        drivetrain.turn_for(LEFT, abs(turnRadius), DEGREES, wait=True)
        print("turning left for ", abs(turnRadius), " degrees")
        brain.screen.set_cursor(3,3)
        brain.screen.print(turnRadius)
        turnTo(turnRadius, "L")

#Check funciton: checks for opening for direction inputed, returns true if there is an opening
def check(direction, dist = distanceThreshold):
    if direction == "L":
        if distanceThreshold < distance_left.object_distance(INCHES):
            return True
        else: return False 
    if direction == "F":
        if distanceThreshold < distance_frontL.object_distance(INCHES):
            return True
        else: return False 
    if direction == "R":
        if distanceThreshold < distance_right.object_distance(INCHES):
            return True
        else: return False 



#May need to verify if something is an intersection


"""
#Finds enter of left opening and turns down it

def findLeftOpening():
   
    closeOpening = 0
    farOpening = 0
    middleOpening = 0
    d = 0
    while check("L") == True:
        drivetrain.drive_for(REVERSE, 1, INCHES, True)
    drivetrain.drive_for(FORWARD, 4, INCHES, True)

    brain.screen.print(distance_left.object_distance(INCHES))
    while check("L") == True:
        drivetrain.drive_for(FORWARD, 1, INCHES, True)
        d += 1
    farOpening = d

    middleOpening = (farOpening / 2) + 1
    drivetrain.drive_for(REVERSE, middleOpening, INCHES, True)
    drivetrain.turn_for(LEFT, 90, DEGREES, False)
    wait(1, SECONDS)
"""


def lookForOpening(isDeadEnd = False):
    lookDist = 7
    touchLed.set_color(Color.GREEN)
    if isDeadEnd == True:
        brain.screen.set_cursor(2,1)
        brain.screen.print("Dead End IF Processed")
        turnTo(90)
    else:
        turnTo(110, "L")
    i = 0
    end = 0
    while i < 8:           #12 for a full circle 
        brain.screen.set_cursor(3,1)
        brain.screen.print(i)
        if check("F", lookDist) == True:
            while check("F", lookDist) == True:
                turnTo(20, "L")
                #drivetrain.turn_for(LEFT, 5, DEGREES, True)
            turnTo(20)
            #drivetrain.turn_for(RIGHT, 5, DEGREES, True)
            while check("F", lookDist) == True:
                turnTo(20)
                end += 20
                #drivetrain.turn_for(RIGHT, 5, DEGREES, True)
            #end = brain_inertial.heading()
            wait(2,SECONDS)
            center = end / 2
            turnTo(center, "L")
            if check("F", lookDist):
                return True
            else: 
                brain.screen.set_cursor(5,1)
                brain.screen.print("Check Front FALSE")

                wait(8, SECONDS)
                return False
        else:
            i += 1
            turnTo(30)
    return False



#Lane Centering
def centerDrive(driveDistance):
    dl = distance_left.object_distance(INCHES)
    if dl < 2:
        drivetrain.turn_for(RIGHT, 15, DEGREES, wait=True)
        drivetrain.drive_for(FORWARD, driveDistance, INCHES, wait=True)
        drivetrain.turn_for(LEFT, 15, DEGREES, wait=True)

    elif dl > 5:
        drivetrain.turn_for(LEFT, 15, DEGREES, wait=True)
        drivetrain.drive_for(FORWARD, driveDistance, INCHES, wait=True)
        drivetrain.turn_for(RIGHT, 15, DEGREES, wait=True)
    else:
        drivetrain.drive_for(FORWARD, driveDistance, INCHES, wait=True)



def center_intersection():
    while check("L") == True:
        #drivetrain.set_drive_velocity(15, PERCENT)
        drivetrain.drive(REVERSE)
    drivetrain.drive_for(FORWARD, 3, INCHES)

"""
#Learning maze Logic
def learnMaze():
    if check("L"):
        #Code to turn robot left 
    elif check("F"):
        #Code to drive forward
    else:
        #code to U turn 
"""

while True:
    if check("L"):
        touchLed.set_color(Color.BLUE)
        center_intersection()
        lookForOpening()
        drivetrain.drive_for(FORWARD, 3, INCHES)
        centerDrive(1)
    elif check("F"):
        touchLed.set_color(Color.GREEN)
        centerDrive(1)
    elif lookForOpening() == True:
        touchLed.set_color(Color.ORANGE)
        drivetrain.drive_for(FORWARD, 3, INCHES)
        centerDrive(1)
    else:
        touchLed.set_color(Color.RED)
        lookForOpening(False)    














#Testing Section 
"""
while True:
    wait(2, SECONDS)
    brain.screen.clear_screen()
    brain.screen.set_cursor(1,1)
    if check("L") == True:
        brain.screen.print("Opening Left")
        lookForOpening()
        drivetrain.drive_for(FORWARD, 2, INCHES, True)
    elif check("F") == True:
        brain.screen.print("Opening Front")
        centerDrive(2)
        #drivetrain.drive_for(FORWARD, 5, INCHES, True)
    elif lookForOpening() == True:
        brain.screen.print("Found one right")
        brain.screen.print("========")
        drivetrain.drive_for(FORWARD, 2, INCHES, True)
    else:
        brain.screen.print("Dead end")
        #Dead End, returns 
        lookForOpening(True)
"""


"""
while True:
    brain.screen.clear_screen()
    brain.screen.set_cursor(3,3)
    brain.screen.print(distance_front.object_distance(INCHES))
    wait(20, MSEC)

"""
