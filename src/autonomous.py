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
motor_arm = Motor(Ports.PORT10, True)
motor_claw = Motor(Ports.PORT9, False)
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
def calibrate():
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

    drivetrain.set_stopping(BRAKE)
    drivetrain.set_heading(0.0, DEGREES)
    drivetrain.set_rotation(0.0, DEGREES)

    wait(3, SECONDS)
    
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)
    brain.play_sound(SoundType.TADA)

    return

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

def adjustHeading(goalHeading):
    currentHeading = brain_inertial.heading()

    if currentHeading != goalHeading:
        brain.screen.print("Adjusting Heading")
        print("Adjusting Heading")
        drivetrain.stop()
        drivetrain.set_turn_velocity(15, PERCENT)
        drivetrain.turn_to_heading(goalHeading, DEGREES, wait=True)
        brain.screen.clear_screen()
    
    return

def sodaCanGrabTask():
    wait(1, SECONDS)
    touchled_nextTask.set_color(Color.GREEN)
    moveArm(0)
    openClaw()
    wait(1, SECONDS)
    closeClaw()
    wait(1, SECONDS)
    moveArm(200)
    wait(1, SECONDS)
    drivetrain.set_drive_velocity(20, PERCENT)
    drivetrain.drive_for(FORWARD, 22, INCHES, wait=True)
    moveArm(45)
    openClaw()
    drivetrain.set_drive_velocity(110, PERCENT)
    drivetrain.drive_for(REVERSE, 22, INCHES, wait=True)
    blockGrabTask()
 
def blockGrabTask():
    wait(3, SECONDS)
    touchled_nextTask.set_color(Color.BLUE)
    drivetrain.set_drive_velocity(20, PERCENT)
    moveArm(150)
    openClaw()
    brain_inertial.set_heading(0, DEGREES)
    drivetrain.drive_for(FORWARD, 10, INCHES, wait=True)
    adjustHeading(0)
    moveArm(0)
    drivetrain.drive_for(FORWARD, 8, INCHES, wait=True)
    closeClaw()
    wait(1, SECONDS)
    moveArm(110)
    drivetrain.drive_for(FORWARD, 5, INCHES, wait=True)
    moveArm(30)
    wait(300, MSEC)
    openClaw()
    moveArm(180)
    drivetrain.set_drive_velocity(110, PERCENT)
    drivetrain.drive_for(REVERSE, 24, INCHES, wait=True)
    return

# def blockKnockOverTask():
#     wait(3, SECONDS)
#     drivetrain.set_drive_velocity(110, PERCENT)
#     touchled_nextTask.set_color(Color.ORANGE)
#     moveArm(75)
#     drivetrain.drive_for(FORWARD, 14, INCHES, wait=True)
#     openClaw()
#     wait(500, MSEC)
#     closeClaw()
#     drivetrain.drive_for(REVERSE, 14, INCHES, wait=True)
#     return

def hookTask():
    wait(1, SECONDS)
    drivetrain.set_drive_velocity(20, PERCENT)
    touchled_nextTask.set_color(Color.RED)
    brain_inertial.set_heading(0, DEGREES)
    moveArm(180)
    openClaw()
    drivetrain.drive_for(FORWARD, 30, INCHES, wait=True)
    drivetrain.set_turn_velocity(25, PERCENT)
    drivetrain.turn_to_heading(65, DEGREES, wait=True)
    wait(500, MSEC)
    adjustHeading(65)
    moveArm(20)
    drivetrain.drive_for(FORWARD, 14, INCHES, wait=True)
    closeClaw()
    wait(500, MSEC)
    moveArm(160)
    brain_inertial.set_heading(180, DEGREES)
    drivetrain.drive_for(REVERSE, 8, INCHES, wait=True)
    drivetrain.turn_to_heading(300, DEGREES)
    wait(500, MSEC)
    adjustHeading(300)
    drivetrain.set_drive_velocity(110, PERCENT)
    drivetrain.drive_for(FORWARD, 36, INCHES, wait=True)
    return

def autonomousChallenge():    
    try:
        drivetrain.set_drive_velocity(20, PERCENT)
        sodaCanGrabTask()

        touchled_nextTask.pressed(hookTask)

        brain.play_sound(SoundType.TADA)

    except Exception as e:
        brain.screen.print("Error!")
        brain.screen.next_row()
        brain.screen.print(e)
        print("Error! ", e)

autonomousChallenge()
