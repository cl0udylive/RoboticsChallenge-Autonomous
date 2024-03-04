# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       ecweyer                                                      #
# 	Created:      3/4/2024, 8:13:56 AM                                         #
# 	Description:  IQ2 project                                                  #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

# Brain should be defined by default
brain = Brain()

def foo():
  brain.screen.print("Button Pressed")

brain.screen.print("Hello IQ2")
brain.buttonCheck.pressed(foo)