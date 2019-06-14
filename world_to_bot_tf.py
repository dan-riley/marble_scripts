#!/usr/bin/env python
import rospy
import tf
# from nav_msgs.msg import *
# from geometry_msgs.msg import *
from gazebo_msgs.srv import GetLinkState

if __name__ == '__main__':
    rospy.init_node('tf_X_broadcaster')
    botframe1 = 'X1/base_link'
    botframe2 = 'X2/base_link'

    br = tf.TransformBroadcaster()
    rospy.wait_for_service('/gazebo/get_link_state')
    gazebo_link_state = rospy.ServiceProxy('/gazebo/get_link_state', GetLinkState)
    rate = rospy.Rate(120)  # 120hz
    while not rospy.is_shutdown():
        try:
            X1_state = gazebo_link_state('X1::X1/base_link', 'world')
            # print(X1_state.link_state.pose.position)
            br.sendTransform((X1_state.link_state.pose.position.x,
                              X1_state.link_state.pose.position.y,
                              X1_state.link_state.pose.position.z),
                             (X1_state.link_state.pose.orientation.x,
                              X1_state.link_state.pose.orientation.y,
                              X1_state.link_state.pose.orientation.z,
                              X1_state.link_state.pose.orientation.w),
                             rospy.Time.now(),
                             botframe1,
                             "world")

            X2_state = gazebo_link_state('X2::X2/base_link', 'world')
            br.sendTransform((X2_state.link_state.pose.position.x,
                              X2_state.link_state.pose.position.y,
                              X2_state.link_state.pose.position.z),
                             (X2_state.link_state.pose.orientation.x,
                              X2_state.link_state.pose.orientation.y,
                              X2_state.link_state.pose.orientation.z,
                              X2_state.link_state.pose.orientation.w),
                             rospy.Time.now(),
                             botframe2,
                             "world")

            rate.sleep()
        except:
            print('Could not send X1/base_link to world transform')
            break
    rospy.spin()
