#! /usr/bin/env python3
# coding:utf-8
#

import rospy
import numpy as np
import sys

print(sys.path)


def main():
    rospy.init_node('rospyhello')
    print("hello world from ros py")

if __name__ == "__main__":
    main()



