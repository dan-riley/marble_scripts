#!/usr/bin/env python
import sys
import rospy
from nav_msgs.msg import Odometry
from gazebo_msgs.srv import GetLinkState


class LinkStateToOdometry:
    def getLinkState(self):  # Position subscriber callback function
        XX_state = self.gazebo_link_state(self.link_name, 'world2')
        self.Odometry.pose.pose = XX_state.link_state.pose
        self.Odometry.twist.twist = XX_state.link_state.twist
        self.Odometry.pose.pose.position.z += 0.4

        # Add time stamp
        self.Odometry.header.stamp = rospy.Time.now()

        return

    def start(self):
        rate = rospy.Rate(50.0)  # 50Hz
        while not rospy.is_shutdown():
            rate.sleep()
            self.getLinkState()
            self.pub1.publish(self.Odometry)
        return

    def __init__(self, link_name="base_link", topic_name="odometry", robot_name="X2", frame="world2", child_frame="X2/base_link"):

        node_name = topic_name + "_" + robot_name
        rospy.init_node(node_name)

        self.link_name = robot_name + "::" + robot_name + "/" + link_name
        self.pubTopic1 = "/" + robot_name + "/" + topic_name
        self.pub1 = rospy.Publisher(self.pubTopic1, Odometry, queue_size=10)

        # Initialize Odometry message object
        self.Odometry = Odometry()
        self.Odometry.header.seq = 1
        self.Odometry.header.frame_id = frame
        self.Odometry.child_frame_id = child_frame

        # Initialize Gazebo LinkState service
        rospy.wait_for_service('/gazebo/get_link_state')
        self.gazebo_link_state = rospy.ServiceProxy('/gazebo/get_link_state', GetLinkState, persistent=True)


if __name__ == '__main__':
    publish_tool = LinkStateToOdometry(robot_name=sys.argv[1], child_frame=sys.argv[1] + "/base_link")

    try:
        publish_tool.start()
    except rospy.ROSInterruptException:
        pass
