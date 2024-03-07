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
heading = brain_inertial.heading()
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

# Select Challenge Dialogue
brain.play_sound(SoundType.ALARM)
brain.screen.print("Select Challenge:")
brain.screen.next_row()
brain.screen.print("Left: Maze")
brain.screen.next_row()
brain.screen.print("Right: Auto.")

# Set Challenge State
mazeChallengeState = True
autoChallengeState = False

# Select Challenge Logic
# def selectMaze():
#     brain.play_note(2, 5, 500)
#     brain.screen.clear_screen()
#     brain.screen.set_cursor(1, 1)
#     brain.screen.print("Maze Selected")
   
#     wait(3, SECONDS)

#     brain.screen.clear_screen()
#     brain.screen.set_cursor(1, 1)

#     mazeChallengeState = True
#     print("Maze State: ", mazeChallengeState)
#     return False
 
# controller.buttonLUp.pressed(selectMaze)

# Call mazeChallenge function if challenge is selected

def selectAuto():
    brain.play_note(1, 5, 500)
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.screen.print("Auto. Selected")
   
    wait(3, SECONDS)

    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)

    autoChallengeState = True

controller.buttonRUp.pressed(selectAuto)

# Maze Challenge Logic
def frontSensorCheck():
    distanceFront = distance_front.object_distance(MM)

    print("Checking Front Sensor")

    # Is there an object in front of the robot?
    while distaÅnceFront < 100:
        brain.screen.print("Object Front!")
        drivetrain.stop()
        sideSensorCheck()
    # No object, drive forward
    brain.screen.print("Driving...")
    drivetrain.set_drive_velocity(100, PERCENT)
    drivetrain.drive(FORWARD)

def sideSensorCheck():
    distanceLeft = distance_left.object_distance(MM)
    distanceRight = distance_right.object_distance(MM)

    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)

    # Is there an object on both sides of the robot?
    if distanceLeft < 100 and distanceRight < 100:
        brain.screen.print("Object Both Sides!")
        drivetrain.stop()
        wait(1, SECONDS)
        brain.screen.next_row()
        # Randomly Turn Left or Right to Explore possibly alternate paths & ensure Robot is not caught in a loop
        print("Dead End Random")
        if random.choice([True, False]):
            brain.screen.print("Turning Left!")
            drivetrain.set_turn_velocity(65, PERCENT)
            drivetrain.turn_for(LEFT, heading + 90, DEGREES, wait=True)
        else:
            brain.screen.print("Turning Right!")
            drivetrain.set_turn_velocity(65, PERCENT)
            drivetrain.turn_for(RIGHT, heading + 90, DEGREES, wait=True)
        
    # Is there an object on only one side of the robot?
    elif distanceLeft < 100 or distanceRight < 100:
        # Is there an object on the left?
        if distanceLeft < 100:
            brain.screen.print("Turning Right!")
            drivetrain.set_turn_velocity(65, PERCENT)
            drivetrain.turn_for(RIGHT, heading + 90, DEGREES, wait=True)
        # Is there an object on the right?
        elif distanceRight < 100:
            brain.screen.print("Turning Left!")
            drivetrain.set_turn_velocity(65, PERCENT)
            drivetrain.turn_for(LEFT, heading + 90, DEGREES, wait=True)
        else:
            brain.screen.print("Error!") 
        
    # Is there no object on either side?
    else:
        # Randomly Turn Left or Right to Explore possibly alternate paths & ensure Robot is not caught in a loop
        print("Intersection Random")
        if random.choice([True, False]):
            brain.screen.print("Turning Left!")
            drivetrain.set_turn_velocity(65, PERCENT)
            drivetrain.turn_for(LEFT, heading + 90, DEGREES, wait=True)
        else:
            brain.screen.print("Turning Right!")
            drivetrain.set_turn_velocity(65, PERCENT)
            drivetrain.turn_for(RIGHT, heading + 90, DEGREES, wait=True)
    
    frontSensorCheck()

# Challenge Function and Loop
def mazeChallenge():
    while True:
        brain.screen.clear_screen()
        brain.screen.set_cursor(1, 1)
        frontSensorCheck()

if mazeChallengeState == True:
    print("Maze Challenge Condition Met")
    mazeChallenge()

##### TODO: Create logic to ensure robot is moving completely straight (Check if distance is equal between left and right sensor and correct),
########### Handle turns better to ensure robot is not stuck, Handle dead ends better and potentially log positions for more intuitive backtracking
########### and maze exploration, handle intersections better (No objects anywhere, or no objects to the sides), clean code up
