#! /usr/bin/env python3
# coding:utf-8
#

import rospy
import sensor_msgs
from sensor_msgs.msg import Image
import numpy as np
import sys
import torch

print(sys.path)

def callback_image(data):
    rospy.loginfo("data from image topic")
    # print(data.data)


def main():
    rospy.init_node('global-localization')
    print("hello world from ros py")
    rospy.Subscriber("/camera/color/image_raw", Image, callback_image)

    rospy.spin()



if __name__ == "__main__":
    main()


