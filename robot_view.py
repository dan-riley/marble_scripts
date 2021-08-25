#!/usr/bin/env python
from __future__ import print_function
import math
import numpy as np

from geometry_msgs.msg import Point
from tf.transformations import quaternion_matrix
from visualization_msgs.msg import Marker


class RobotView:

    def __init__(self, pose, viewRange):

        self.robot_view_pub = rospy.Publisher('robot_view', Marker, queue_size=10)

        # View parameters
        self.range = viewRange
        hfov = 70.0
        vfov = 40.0
        hfov_rad = hfov * math.pi / 180.0
        vfov_rad = vfov * math.pi / 180.0
        self.height = 2.0 * math.tan(vfov_rad / 2.0) * self.range
        self.width = 2.0 * math.tan(hfov_rad / 2.0) * self.range

        # Extract the position and orientation vectors
        self.pos = np.array([pose.position.x, pose.position.y, pose.position.z])
        quat = pose.orientation
        self.matrix = quaternion_matrix([quat.x, quat.y, quat.z, quat.w])

        self.buildVectors()
        self.buildCorners()
        self.buildPlanes()
        self.pubView()

    def buildVectors(self):
        self.view = np.array([self.matrix[0][0], self.matrix[1][0], self.matrix[2][0]])
        self.right = np.array([self.matrix[0][1], self.matrix[1][1], self.matrix[2][1]])
        self.up = np.array([self.matrix[0][2], self.matrix[1][2], self.matrix[2][2]])

    def buildCorners(self):
        self.fp_c = self.pos + self.view * self.range
        self.fp_tl = self.fp_c + (self.up * self.height / 2) + (self.right * self.width /2)
        self.fp_tr = self.fp_c + (self.up * self.height / 2) - (self.right * self.width /2)
        self.fp_bl = self.fp_c - (self.up * self.height / 2) + (self.right * self.width /2)
        self.fp_br = self.fp_c - (self.up * self.height / 2) - (self.right * self.width /2)

    def buildPlanes(self):
        self.pl_f = (self.fp_bl - self.fp_br).cross(self.fp_tr - self.fp_br)

    def pubView(self):
        pubview = Marker()
        pubview.header.frame_id = "world"
        pubview.scale.x = 1.0
        pubview.scale.y = 1.0
        pubview.scale.z = 1.0
        pubview.color.a = 0.85
        pubview.color.r = 0.0
        pubview.color.g = 191.0/255.0
        pubview.color.b = 1.0
        pubview.type = 11
        pubview.action = pubview.ADD

        robot = Point()
        robot.x = self.pos[0]
        robot.y = self.pos[1]
        robot.z = self.pos[2]
        TL = Point()
        TL.x = self.fp_tl[0]
        TL.y = self.fp_tl[1]
        TL.z = self.fp_tl[2]
        TR = Point()
        TR.x = self.fp_tr[0]
        TR.y = self.fp_tr[1]
        TR.z = self.fp_tr[2]
        BL = Point()
        BL.x = self.fp_bl[0]
        BL.y = self.fp_bl[1]
        BL.z = self.fp_bl[2]
        BR = Point()
        BR.x = self.fp_br[0]
        BR.y = self.fp_br[1]
        BR.z = self.fp_br[2]

        pubview.points.append(robot)
        pubview.points.append(TL)
        pubview.points.append(BL)
        pubview.points.append(robot)
        pubview.points.append(TL)
        pubview.points.append(TR)
        pubview.points.append(robot)
        pubview.points.append(TR)
        pubview.points.append(BR)
        pubview.points.append(robot)
        pubview.points.append(BR)
        pubview.points.append(BL)
        self.robot_view_pub.publish(pubview)
