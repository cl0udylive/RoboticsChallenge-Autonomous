#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code
brain_inertial = Inertial()
left_drive_smart = Motor(Ports.PORT7, 3.0, True)
right_drive_smart = Motor(Ports.PORT12, 3.0, False)

drivetrain = SmartDrive(left_drive_smart, right_drive_smart, brain_inertial, 200)
motor_claw = Motor(Ports.PORT11, False)
motor_arm = Motor(Ports.PORT10, False)
touchled_nextTask = Touchled(Ports.PORT8)



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
# 	Project:      Autonomous Task Challenge
# 	Author:       Eli Weyer
# 	Created:      March 21 2024
# 	Description:  Source code for the Autonomous Task Robot. 
#                 Created for New Visions Engineering 
#                 Robotics Challenge.
# 
# ------------------------------------------

# Library imports
from vex import *

# Begin project code
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
touchled_nextTask.set_brightness(100)
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
drivetrain.set_stopping(BRAKE)
drivetrain.set_heading(0.0, DEGREES)
drivetrain.set_rotation(0.0, DEGREES)

brain.play_note(4, 5, 500)
brain.screen.print("Devices:")
brain.screen.next_row()
brain.screen.print(drivetrain)
brain.screen.next_row()
brain.screen.print(motor_claw)
brain.screen.next_row()
brain.screen.print(motor_arm)
brain.screen.next_row()
brain.screen.print(touchled_nextTask)
wait(3, SECONDS)

brain.screen.clear_screen()
brain.screen.set_cursor(1, 1)

# Autonomous Task Logic
def closeClaw():
    motor_claw.spin(FORWARD)

def openClaw():
    motor_claw.spin(REVERSE)

def moveArm(armAngle):
    motor_arm.spin_to_position(armAngle, DEGREES, wait=True)

def sodaCanGrabTask():
    touchled_nextTask.set_color(Color.GREEN)
    moveArm(0)
    openClaw()
    wait(1, SECONDS)
    closeClaw()
    wait(1, SECONDS)
    moveArm(-200)
    wait(1, SECONDS)
    drivetrain.drive_for(FORWARD, 20, INCHES, wait=True)
    moveArm(-45)
    wait(1, SECONDS)
    openClaw()
    drivetrain.drive_for(REVERSE, 20, INCHES, wait=True)
    return

    
def blockGrabTask():
    touchled_nextTask.set_color(Color.GREEN)
    moveArm(-5)
    openClaw()
    wait(1, SECONDS)
    drivetrain.drive_for(FORWARD, 18, INCHES, wait=True)
    closeClaw()
    wait(1, SECONDS)
    moveArm(-100)
    wait(1, SECONDS)
    drivetrain.drive_for(FORWARD, 6, INCHES, wait=True)
    moveArm(-25)
    wait(1, SECONDS)
    openClaw()
    moveArm(-40)
    wait(3, SECONDS)
    drivetrain.drive_for(REVERSE, 2, INCHES, wait= True)
    hookTask()
    return

def hookTask():
    # TODO: Logic for Hook Task
    print("Hook Task")
    closeClaw()
    wait(1, SECONDS)
    drivetrain.set_turn_velocity(50, PERCENT)
    drivetrain.turn_for(RIGHT, 45, DEGREES, wait=True)
    print("Turn")
    drivetrain.drive_for(FORWARD, 10, INCHES, wait=True)
    print("drive")
    drivetrain.turn_for(RIGHT, 20, DEGREES, wait=True)
    moveArm(-45)
    wait(1, SECONDS)
    openClaw()
    wait(1, SECONDS)
    drivetrain.drive_for(FORWARD, 16, INCHES, True)
    closeClaw()
    wait(1, SECONDS)
    moveArm(-100)
    wait(1, SECONDS)
    return

def autonomousChallenge():
    drivetrain.set_drive_velocity(30, PERCENT)

    try:
        #sodaCanGrabTask()
        touchled_nextTask.set_color(Color.WHITE)
        touchled_nextTask.set_fade(FadeType.FAST)
        touchled_nextTask.pressed(blockGrabTask)
        brain.play_sound(SoundType.TADA)

    except Exception as e:
        brain.screen.print("Error!")
        brain.screen.next_row()
        brain.screen.print(e)
        print("Error! ", e)

autonomousChallenge()
