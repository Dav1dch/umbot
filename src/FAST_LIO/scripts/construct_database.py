#! /usr/bin/env python3
# coding:utf-8
#

import rospy
import sensor_msgs
from sensor_msgs.msg import Image

import torch
import torchvision
import numpy as np
import os

print(os.getcwd())

model = torchvision.models.resnet18(weights=torchvision.models.ResNet18_Weights)
model = model.eval()

timestamps = []
embeddings = []

def callback_db(data):
    rospy.loginfo("receive image")
    im = np.frombuffer(data.data, dtype=np.uint8).reshape(data.height, data.width, -1)
    im = torch.from_numpy(im).type(dtype=torch.float)
    with torch.no_grad():
        stamp = str(data.header.stamp.secs) + "." + str(data.header.stamp.nsecs)
        timestamps.append(stamp)
        # print(data.header)
        embedding = model(im.unsqueeze(0).view(1,3 , 640, 480))
        embeddings.append(embedding.numpy())
    # print(model(data.data))
    np.save("/root/Code/umbot/src/FAST_LIO/scripts/timestamps.npy", timestamps)
    np.save("/root/Code/umbot/src/FAST_LIO/scripts/embeddings.npy", embeddings)

def main():
    rospy.init_node('construct-database')
    rospy.Subscriber("/camera/color/image_raw", Image, callback_db)
    rospy.spin()


    return

if __name__ == "__main__":
    main()

