#!/usr/bin/env python
import sys
import rospy
import tf
from nav_msgs.msg import Odometry

class TransformToOdometry:
    def getTransform(self):
        try:
            (trans, rot) = self.listener.lookupTransform(self.Odometry.header.frame_id, self.Odometry.child_frame_id, rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            return 
        
        self.Odometry.pose.pose.position.x = trans[0]
        self.Odometry.pose.pose.position.y = trans[1]
        self.Odometry.pose.pose.position.z = trans[2]
        
        self.Odometry.pose.pose.orientation.x = rot[0]
        self.Odometry.pose.pose.orientation.y = rot[1]
        self.Odometry.pose.pose.orientation.z = rot[2]
        self.Odometry.pose.pose.orientation.w = rot[3]

        # Add time stamp
        self.Odometry.header.stamp = rospy.Time.now()

        return

    def start(self):
        rate = rospy.Rate(10.0)  # 50Hz

        while not rospy.is_shutdown():
            rate.sleep()
            self.getTransform()
            self.pub1.publish(self.Odometry)
        return

    def __init__(self, link_name="base_link", topic_name="odometry", robot_name="X1", frame="world", child_frame="X1/base_link"):

        node_name = topic_name + "_" + robot_name
        rospy.init_node(node_name)

        self.listener = tf.TransformListener()
        self.pubTopic1 = "/" + robot_name + "/" + topic_name
        self.pub1 = rospy.Publisher(self.pubTopic1, Odometry, queue_size=10)

        # Initialize Odometry message object
        self.Odometry = Odometry()
        self.Odometry.header.seq = 1
        self.Odometry.header.frame_id = frame
        self.Odometry.child_frame_id = child_frame


if __name__ == '__main__':
    publish_tool = TransformToOdometry(robot_name=sys.argv[1], child_frame=sys.argv[1] + "/base_link")

    try:
        publish_tool.start()
    except rospy.ROSInterruptException:
        pass
