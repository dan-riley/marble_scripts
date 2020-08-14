#!/usr/bin/env python

"""
Used for testing the gui. 

Publishes an array of Artifacts and publishes an image for one of those
artifacts in the following two formats
  1. rqt format: For rqt to detect and view compressed images, it requires:
    * the topic is of type sensor_msgs::CompressedImage. Only topics whose type is 
      sensor_msgs::CompressedImage will be detected and not attributes of messages 
      whose type is sensor_msgs::CompressedImage
    * the topic name ends with the suffix "/compressed" 
  2. gui format: it requires
    * the compressed image to be an atribute of ArtifactImg so other information
      can be bundled with it, such as artifact_id and robot name


This node shares some of the same functionality as the 
marble/marble_artifact_detection/src/publish_artifacts.cpp node.
Both files are kept for reference in case we decide to do things in C++ or python.

"""

import rospy
from marble_artifact_detection_msgs.msg import Artifact, ArtifactArray
from sensor_msgs.msg import CompressedImage
import cv2
from cv_bridge import CvBridge
import numpy as np

ROBOT_NAME = 'X1'

def get_messages_filled_with_data():
    array_msg = ArtifactArray()
    survivor_img_msg = CompressedImage()
    extinguisher_img_msg = CompressedImage()
    drill_img_msg = CompressedImage()
    backpack_img_msg = CompressedImage()

    cv_img = cv2.imread('survivor.jpg', cv2.IMREAD_COLOR)
    survivor_img_msg = CvBridge().cv2_to_compressed_imgmsg(cv_img)
    cv_img = cv2.imread('extinguisher.jpg', cv2.IMREAD_COLOR)
    extinguisher_img_msg = CvBridge().cv2_to_compressed_imgmsg(cv_img)
    cv_img = cv2.imread('drill.jpg', cv2.IMREAD_COLOR)
    drill_img_msg = CvBridge().cv2_to_compressed_imgmsg(cv_img)
    cv_img = cv2.imread('backpack.jpg', cv2.IMREAD_COLOR)
    backpack_img_msg = CvBridge().cv2_to_compressed_imgmsg(cv_img)

    array_msg.header.seq = 1
    array_msg.header.stamp = rospy.Time.now()
    array_msg.header.frame_id = ''
    array_msg.owner = ROBOT_NAME

    for i in range(1, 20):
        msg = Artifact()
        msg.header.seq = i
        msg.header.stamp = rospy.Time.now()
        msg.header.frame_id = ''
        msg.artifact_id = ROBOT_NAME + '_' + str(i)
        msg.position.x = 0
        msg.position.y = 0
        msg.position.z = 0
        msg.obj_class = ''
        msg.obj_prob = 0
        array_msg.artifacts.append(msg)

    array_msg.artifacts[0].position.x = 70
    array_msg.artifacts[0].position.y = -3.9
    array_msg.artifacts[0].position.z = 0.2
    array_msg.artifacts[0].obj_class = 'backpack'
    array_msg.artifacts[0].image_data = backpack_img_msg
    array_msg.artifacts[0].obj_prob = 0.785

    array_msg.artifacts[1].position.x = 25
    array_msg.artifacts[1].position.y = 2.0
    array_msg.artifacts[1].position.z = 0.2
    array_msg.artifacts[1].obj_class = 'drill'
    array_msg.artifacts[1].image_data = drill_img_msg
    array_msg.artifacts[1].obj_prob = 0.454

    array_msg.artifacts[2].position.x = 60.0
    array_msg.artifacts[2].position.y = -2
    array_msg.artifacts[2].position.z = 0.2
    array_msg.artifacts[2].obj_class = 'person'
    array_msg.artifacts[2].image_data = survivor_img_msg
    array_msg.artifacts[2].obj_prob = 0.154

    array_msg.artifacts[3].position.x = 40
    array_msg.artifacts[3].position.y = 20
    array_msg.artifacts[3].position.z = 0.2
    array_msg.artifacts[3].obj_class = 'extinguisher'
    array_msg.artifacts[3].image_data = extinguisher_img_msg
    array_msg.artifacts[3].obj_prob = 0.972

    # array_msg.artifacts[4].position.x = 65
    # array_msg.artifacts[4].position.y = -40
    # array_msg.artifacts[4].position.z = 0.2
    # array_msg.artifacts[4].obj_class = 'extinguisher'
    # array_msg.artifacts[4].image_data = extinguisher_img_msg
    # array_msg.artifacts[4].obj_prob = 0.972
    #
    # array_msg.artifacts[5].position.x = 15
    # array_msg.artifacts[5].position.y = -60
    # array_msg.artifacts[5].position.z = 0.2
    # array_msg.artifacts[5].obj_class = 'extinguisher'
    # array_msg.artifacts[5].image_data = extinguisher_img_msg
    # array_msg.artifacts[5].obj_prob = 0.972

    return array_msg


rospy.init_node('fake_artifact_array_pub', anonymous=True)

array_pub = rospy.Publisher('/' + ROBOT_NAME + '/artifact_array', ArtifactArray, queue_size=10)

array_msg = get_messages_filled_with_data()

rate = rospy.Rate(1)
while not rospy.is_shutdown():
    array_pub.publish(array_msg)
    rate.sleep()
