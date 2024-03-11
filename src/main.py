#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code
brain_inertial = Inertial()



# Make random actually random
def setRandomSeedUsingAccel():
    wait(100, MSEC)
    xaxis = brain_inertial.acceleration(XAXIS) * 1000
    yaxis = brain_inertial.acceleration(YAXIS) * 1000
    zaxis = brain_inertial.acceleration(ZAXIS) * 1000
    urandom.seed(int(xaxis + yaxis + zaxis))
    
# Set random seed 
setRandomSeedUsingAccel()

#endregion VEXcode Generated Robot Configuration

# ------------------------------------------
# 
# 	Project:      Self Driving Robot 
# 	Author:       Eli Weyer
# 	Created:      3/5/24
# 	Description:  Source code for a Self Driving Robot. 
#                 Created for New Visions Engineering 
#                 Robotics Challenge.
#   Updated:      3/7/24
# 
# ------------------------------------------

# Import Random Library
import random

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
currentHeading = brain_inertial.heading()
wait(5, SECONDS)

brain.screen.clear_screen()
brain.screen.set_cursor(1, 1)
brain.play_sound(SoundType.TADA)
brain.screen.print("Complete!")
wait(2, SECONDS)

brain.screen.clear_screen()
brain.screen.set_cursor(1, 1)

# Initialize and Calibrate Robot Sensors and Devices
drivetrain.set_stopping(HOLD)
drivetrain.set_heading(0.0, DEGREES)
drivetrain.set_rotation(0.0, DEGREES)

brain.play_note(4, 5, 500)
brain.screen.print("Devices:")
brain.screen.next_row()
brain.screen.print(drivetrain)
brain.screen.next_row()
brain.screen.print(controller)
brain.screen.next_row()
brain.screen.print(distance_front)
brain.screen.next_row()
brain.screen.print(distance_left)
brain.screen.next_row()
brain.screen.print(distance_right)
wait(3, SECONDS)

brain.screen.clear_screen()
brain.screen.set_cursor(1, 1)

# Maze Challenge Logic
def handleSingleObstacle(isObstacleLeft):
    if isObstacleLeft:
        handleObstacle("left")
    else:
        handleObstacle("right")

def handleObstacle(obstacleDirection):

    if obstacleDirection == "front":
        brain.screen.print("Object Front!")
        print("Object Front!")
        drivetrain.stop()
        sideSensorCheck()

    elif obstacleDirection == "left":
        brain.screen.print("Turning Right!")
        print("Turning Right!")
        drivetrain.set_turn_velocity(65, PERCENT)            
        drivetrain.turn_for(RIGHT, currentHeading + 90, DEGREES, wait=True)

    elif obstacleDirection == "right":
        brain.screen.print("Turning Left!")
        print("Turning Left!")
        drivetrain.set_turn_velocity(65, PERCENT)
        drivetrain.turn_for(LEFT, currentHeading + 90, DEGREES, wait=True)

    elif obstacleDirection == "both":
        print("Intersection!")
        drivetrain.stop()
        randomTurn()

    else:
        print("Dead End!")
        drivetrain.stop()
        randomTurn()

def randomTurn():

    if random.choice([True, False]):
        brain.screen.print("Turning Left!")
        print("Turning Left!")
        drivetrain.set_turn_velocity(65, PERCENT)
        drivetrain.turn_for(LEFT, currentHeading + 90, DEGREES, wait=True)

    else:
        brain.screen.print("Turning Right!")
        print("Turning Right!")
        drivetrain.set_turn_velocity(65, PERCENT)
        drivetrain.turn_for(RIGHT, currentHeading + 90, DEGREES, wait=True)

DISTANCE_THRESHOLD = 100 # millimeters
DRIFT_THRESHOLD = 5 # degrees

def mazeChallenge():
    try:
        while True:
            distanceFront = distance_front.object_distance(MM)
        
            brain.screen.clear_screen()
            brain.screen.set_cursor(1, 1)

            while distanceFront < DISTANCE_THRESHOLD:
                handleObstacle("front")
                break
        
            currentHeading = brain_inertial.heading()
            nearestHeading = round(currentHeading / 90) * 90

            if abs(currentHeading - nearestHeading) > DRIFT_THRESHOLD:
                brain.screen.print("Adjusting Heading")
                print("Adjusting Heading")
                drivetrain.stop()
                drivetrain.set_turn_velocity(65, PERCENT)
                drivetrain.turn_to_heading(nearestHeading, DEGREES, wait=True)

            brain.screen.print("Driving...")
            print("Driving...")
            drivetrain.set_drive_velocity(100, PERCENT)
            drivetrain.drive(FORWARD)

    except Exception as e:
        brain.screen.print("Error!")
        brain.screen.next_row()
        brain.screen.print(e)
        print("Error! ", e)
        

mazeChallenge()

##### Everything below this was made or edited by Thomas

def intersection():   # recursive function called everytime the robot comes across a intersection or dead end 
    openings = findOpenings() 
    wayBackHeading = brain_inertial.heading() - 180;  #heading is stored incase intersection is no good, is passed to goBack function Many need to be normalized to ensure it always falls between 0-360
    openingHeading = wayBackHeading   #robot starts at the opening it came through and updates this var everytime it goes through a new opening 

    if mazecomplete():
            return True;

    if openings == 0:    #Logic is for dead ends, need to rename entire function to better describe it 
        goBack(wayBackHeading)
        return False # goes back to last intersection and then takes one step out of recursive call 
            
    for i in range(openings): #it will try every opening at an intersection
        while objectFront():    
            drivetrain.set_turn_velocity(65, PERCENT)
            drivetrain.turn_to_heading(openingHeading +5, DEGREES, wait=True)       #Logic: spin to current angle - 180 and spin clockwise until first opening is found
        openingHeading = brain_inertial.heading()
        if driveForward():  #returns true when at a dead end or intersection which calls intersection
            intersection() 
        if i == (openings -1): #If all paths in a intersection are bad go back and take one step out of recursive call 
            goBack(wayBackHeading)
            return False
    


def findOpenings():    #Basically does a circle and counts the amount of openings at a intersection, code is probably redundant but it works, hopefully 
    startHeading = brain.inertial.heading()
    x = False                  
    y = False
    count = 0;
    while brain.inertial.heading() != startHeading:
        y = x
        drivetrain.set_turn_velocity(65, PERCENT)
        drivetrain.turn_to_heading(openingHeading +5, DEGREES, wait=True)
        if objectFront() != True:
            x = False
        else 
            x = True

        if x != y:
            count += 1
    return(count)


def goBack(wayBackHeading):
    drivetrain.set_turn_velocity(65, PERCENT)
    drivetrain.turn_to_heading(wayBackHeading, DEGREES, wait=True) #turns around to go back
    driveForward();
    

def driveForward(): #probably needs some sort of lane centering algorithm
    while checkIntersection() != True:  #Function will return true when it comes across an intersection
        drivetrain.set_drive_velocity(100, PERCENT)
        drivetrain.drive(FORWARD)       #how do I control amount driven forward

    
def checkIntersection():
    if sideSensorCheck():
        return True
    if objectFront():
        return True


def sideSensorCheck():   #Made by Eli but changed return values to work for me 
    DISTANCE_THRESHOLD = 100 # millimeters

    distanceLeft = distance_left.object_distance(MM)
    distanceRight = distance_right.object_distance(MM)

    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)

    if distanceLeft > DISTANCE_THRESHOLD and distanceRight > DISTANCE_THRESHOLD:
        return True
    
    elif distanceLeft > DISTANCE_THRESHOLD or distanceRight > DISTANCE_THRESHOLD:
        return True
        
    else:
        return False


def objectFront():  #returns true if object is infront 
    distanceFront = distance_front.object_distance(MM)
    if distanceFront < DISTANCE_THRESHOLD:
        return True

            



