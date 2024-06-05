#! /usr/bin/env python3
# coding:utf-8
#

import rospy
import sensor_msgs
from sensor_msgs.msg import Image

import torch
import torchvision
import numpy as np

model = torchvision.models.resnet18(weights=torchvision.models.ResNet18_Weights)
model = model.eval()

def callback_db(data):
    rospy.loginfo("receive image")
    im = np.frombuffer(data.data, dtype=np.uint8).reshape(data.height, data.width, -1)
    im = torch.from_numpy(im).type(dtype=torch.float)
    with torch.no_grad():
        print(model(im.unsqueeze(0).view(1, 3, 640, 480)))
    # print(model(data.data))

def main():
    rospy.init_node('construct-database')
    rospy.Subscriber("/camera/color/image_raw", Image, callback_db)
    rospy.spin()


    return

if __name__ == "__main__":
    main()

