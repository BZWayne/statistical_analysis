#! /usr/bin/env python

"""
.. module::option3
    :platform: Unix
    :synopsis: Python module for the manual mode with assistance

.. moduleauthor:: Bauyrzhan Zhakanov

This mode allows to use the robot in manual mode. The robot can be controlled with keyboards.
BY receiving the inputs, the robot moves forward/backward, right/left. However, this mode tells
about the distance to the obtacles. Using the /scan to detect the walls around the robot.

"""

import rospy
import time
import os
from move_base_msgs.msg import MoveBaseActionGoal
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from actionlib_msgs.msg import GoalID
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

# function for convenient usage enter inputs
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

    velocity_x = 0
    angular_vel = 0
    exit_system = False
    button = getch()

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

# for detecting the minimal distance until obstacle from all sides
def min_distance(distance_wall):

    """
    This method is used for calculating the distances to the wall
    """

    min_distance = 30
    angle_provided = 45

    # front angle
    for i in range(-angle_provided, angle_provided):
        if distance_wall[i] < min_distance:
            min_distance = distance_wall[i]

    # right angle
    for i in range(-3*angle_provided, -angle_provided+1):
        if distance_wall[i] < min_distance:
            min_distance = distance_wall[i]

    # left angle
    for i in range(angle_provided+1, 3*angle_provided):
        if distance_wall[i] < min_distance:
            min_distance = min_distance[i]

    return min_distance, min_distance, min_distance

# main function for option three
def option_three():

    """
    This method is used for moving robot by pressing the inputs
    /scan is used to detect the obstacles around the robot for its avoidance 
    """

    exit_system = 0
    distance_obst = 1 # Variable to set the minimal safe distance
    welcome()

    msg_twist = Twist()
    msg_twist.linear.y = 0
    msg_twist.linear.z = 0
    msg_twist.angular.x = 0
    msg_twist.angular.y = 0

    # until not exitting from system
    while not exit_system:

        ## start controlling the robot and publish
        [msg_twist.linear.x, msg_twist.angular.z, exit_system] = control_buttons()

        ## consider the laser distance_wall for obstacle avoidance
        laser = rospy.wait_for_message("/scan", LaserScan)
        laser_data = laser.ranges
        [min_left, min_front, min_right] = min_distance(laser_data)

        ## distance to wall from left
        if min_left < distance_obst:
            if msg_twist.angular.z < 0:
                print("Obstacle from the left \n")
                msg_twist.angular.z = 0

        ## distance to wall from front
        elif min_front < distance_obst:
            if msg_twist.linear.x > 0:
                print("Obstacle from the front \n")
                msg_twist.linear.x = 0

        ## distance to wall from right
        elif min_right < distance_obst:
            if msg_twist.angular.z > 0:
                print("Obstacle from the right \n")
                msg_twist.angular.z = 0

        publisher_velocity.publish(msg_twist)

        ## after some time just reset the values
        time.sleep(0.2)
        msg_twist.linear.x = 0
        msg_twist.angular.z = 0
        publisher_velocity.publish(msg_twist)
        print('\033[F' + '\033[K')

    return 1