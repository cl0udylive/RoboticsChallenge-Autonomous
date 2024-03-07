#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code
brain_inertial = Inertial()
left_drive_smart = Motor(Ports.PORT8, 1.0, False)
right_drive_smart = Motor(Ports.PORT11, 1.0, True)

drivetrain = SmartDrive(left_drive_smart, right_drive_smart, brain_inertial, 200)
controller = Controller()
distance_left = Distance(Ports.PORT1)
distance_right = Distance(Ports.PORT6)
distance_front = Distance(Ports.PORT3)



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
# 	Project:      Self Driving Robot 
# 	Author:       Eli Weyer
# 	Created:      3/5/24
# 	Description:  Source code for a Self Driving Robot. 
#                 Created for New Visions Engineering 
#                 Robotics Challenge.
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

# # Select Challenge Dialogue
# brain.play_sound(SoundType.ALARM)
# brain.screen.print("Select Challenge:")
# brain.screen.next_row()
# brain.screen.print("Left: Maze")
# brain.screen.next_row()
# brain.screen.print("Right: Auto.")

# Select Challenge Logic


# Maze Challenge Logic
def handleError():
    brain.screen.print("Error!")
    print("Error")

def handleObstacle(obstacleDirection):

    current_heading = brain_inertial.heading()

    if obstacleDirection == "front":
        brain.screen.print("Object Front!")
        print("Object Front!")
        drivetrain.stop()
        sideSensorCheck()

    elif obstacleDirection == "left":
        brain.screen.print("Turning Right!")
        print("Turning Right!")
        drivetrain.set_turn_velocity(65, PERCENT)            
        drivetrain.turn_for(RIGHT, current_heading + 90, DEGREES, wait=True)

    elif obstacleDirection == "right":
        brain.screen.print("Turning Left!")
        print("Turning Left!")
        drivetrain.set_turn_velocity(65, PERCENT)
        drivetrain.turn_for(LEFT, current_heading + 90, DEGREES, wait=True)

    elif obstacleDirection == "both":
        print("Intersection!")
        drivetrain.stop()
        randomTurn()

    else:
        print("Dead End!")
        drivetrain.stop()
        randomTurn()

def randomTurn():

    current_heading = brain_inertial.heading()

    if random.choice([True, False]):
        brain.screen.print("Turning Left!")
        print("Turning Left!")
        drivetrain.set_turn_velocity(65, PERCENT)
        drivetrain.turn_for(LEFT, current_heading + 90, DEGREES, wait=True)

    else:
        brain.screen.print("Turning Right!")
        print("Turning Right!")
        drivetrain.set_turn_velocity(65, PERCENT)
        drivetrain.turn_for(RIGHT, current_heading + 90, DEGREES, wait=True)

def sideSensorCheck():
    distanceLeft = distance_left.object_distance(MM)
    distanceRight = distance_right.object_distance(MM)

    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)

    if distanceLeft < 100 and distanceRight < 100:
        handleObstacle("both")
    
    elif distanceLeft < 100 or distanceRight < 100:
        
        if distanceLeft < 100:
            handleObstacle("left")

        else:
            handleObstacle("right")
        
    else:
        handleObstacle("all")

def mazeChallenge():
    while True:
        distanceFront = distance_front.object_distance(MM)
        
        brain.screen.clear_screen()
        brain.screen.set_cursor(1, 1)

        while distanceFront < 100:
            handleObstacle("front")
            break
       
        current_heading = brain_inertial.heading()
        print(current_heading)
        nearest_heading = round(current_heading / 90) * 90
        print(nearest_heading)

        if nearest_heading != current_heading:
            drivetrain.stop()
            drivetrain.turn_to_heading(nearest_heading, DEGREES, wait=True)    

        brain.screen.print("Driving...")
        print("Driving...")
        drivetrain.set_drive_velocity(100, PERCENT)
        drivetrain.drive(FORWARD)
        

# Challenge Selector does not work, fix in future
mazeChallenge()

##### TODO: Create logic to ensure robot is moving completely straight (Check if distance is equal between left and right sensor and correct),
########### Handle turns better to ensure robot is not stuck, Handle dead ends better and potentially log positions for more intuitive backtracking
########### and maze exploration, handle intersections better (No objects anywhere, or no objects to the sides), clean code up
