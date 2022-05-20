#! /usr/bin/env python

"""
.. module::master
    :platform Unix
    :synopsis: Python module for managing the robot to the target

..moduleauthor:: Bauyrzhan Zhakanov

This module is responsible for managing the driving modes choosen by user. WIth this user interface, 
the user can choose either autonomous, manual driving and manual driving with assistance. 
This file is calling specific functions in terminal and receive inputs. 

"""

import rospy
import os
from option1 import option_one
from option2 import option_two
from option3 import option_three

# User interface to give the user a set of options
def welcome():
    """
    This is the instruction list for user
    """

    os.system('clear')
    print("Whats Up? This is RT1 Assignment III, and here is an UI for it.")
    print("Press [1] for autonomous drive of the robot")
    print("Press [2] for manual drive of the robot")
    print("Press [3] for manual drive of the robot with collision avoidance")
    print("Press [4] for exitting from the system")


def main():

    """
    This function used to choose the driving mode by user
    #The user message is passed to the service ``master``
    """

    exit_system = False
    rospy.init_node('final_assignment')
    while not rospy.is_shutdown() and not exit_system:
        welcome()
        while True:
            try:
                button = int(input("Choose drive options: "))
                break
            except:
                print("Your input is not possible to obtain")
        if button == 1:
            while not option_one():
                pass
        if button == 2:
            while not option_two():
                pass
        if button == 3:
            while not option_three():
                pass
        elif button == 4:
            exit_system = True
        else:
            print("Wrong button")

if __name__ == '__main__':
    main()