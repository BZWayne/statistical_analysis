#! /usr/bin/env python

"""
.. module::option2
    :platform: Unix
    :synopsis: Python module for the manual mode

.. moduleauthor:: Bauyrzhan Zhakanov

This mode allows to use the robot in manual mode. The robot can be controlled with keyboards.
BY receiving the inputs, the robot moves forward/backward, right/left. 

"""

import rospy
import time
import os
from geometry_msgs.msg import Twist
import termios
import sys, tty

# publisher of velocity
publisher_velocity = rospy.Publisher("cmd_vel", Twist, queue_size = 50)

## welcoming words and instructions
def welcome():

    """
    This is the instruction list of keyboards for user
    """

    os.system('clear')
    print("Manual drive is activated")
    print("Press [W] or [w]: to move forward")
    print("Press [S] or [s]: to move backward")
    print("Press [A] or [a]: to turn left")
    print("Press [D] or [d]: to turn right")
    print("Press [Q] or [q]: to exit from manual drive \n")

## buttons for movement (forward, backward, right, left) and exit
def getch():

    """
    This method getch() is used for avoiding pressing Enter 
    """

    def _getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    return _getch()

# Control buttons for robot
def control_buttons():

    """
    This method is used for controlling the buttons
    Control buttons: forward - backward, right - left, exit
    """

    button = getch()
    velocity_x = 0
    angular_vel = 0
    exit_system = False

    ## buttons for movement (forward, backward, right, left) and exit
    if button == 'w' or button == 'W':
        return 1.0, 0, False
    elif button == 'a' or button == 'A':
        return 0, 2, False
    elif button == 'd' or button == 'D':
        return 0, -2, False
    elif button == 's' or button == 'S':
        return -1.0, 0, False
    elif button == 'q' or button == 'Q':
        return 0, 0, True
    else:
        print("Wrong button \n")
    return velocity_x, angular_vel, exit_system

# main for option_two
def option_two():

    """
    This method is used for moving the robot based on the pressed inputs 
    """

    exit_system = False
    msg_twist = Twist()
    msg_twist.linear.y = 0
    msg_twist.linear.z = 0
    msg_twist.angular.x = 0
    msg_twist.angular.y = 0
    welcome()

    ## loop
    while not exit_system:

        ## start controlling the robot and publish
        [msg_twist.linear.x, msg_twist.angular.z, exit_system] = control_buttons() 
        publisher_velocity.publish(msg_twist) 

        ## after some time stop and reset values for linear abd angular values
        time.sleep(0.2)
        msg_twist.linear.x = 0
        msg_twist.angular.z = 0
        publisher_velocity.publish(msg_twist) 
        print('\033[F' + '\033[K')
    return 1