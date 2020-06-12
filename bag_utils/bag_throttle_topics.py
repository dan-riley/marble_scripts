import sys
import rospy
import rosbag

class ThrottleTopic:
    def __init__(self, name, stamp):
        self.name = name
        self.stamp = stamp

if __name__ == '__main__':
    # Usage: python bag_throttle_topics.py inputfile.bag outputfile.bag

    # List of topics to throttle
    ttopics = ['merged_map', 'octomap_binary', 'camera_map', 'camera_view']
    # Minimum time in seconds between messages to discard
    rate = 1

    inputfile = sys.argv[1]
    if len(sys.argv) == 3:
        outputfile = sys.argv[2]
    else:
        outputfile = 'output.bag'

    Throttled = {}
    with rosbag.Bag(outputfile, 'w') as outbag:
        for topic, msg, t in rosbag.Bag(inputfile).read_messages():
            include = True
            if any(ttopic in topic for ttopic in ttopics):
                if topic not in Throttled:
                    Throttled[topic] = ThrottleTopic(topic, t)
                    include = True
                else:
                    if t >= Throttled[topic].stamp + rospy.Duration(rate):
                        include = True
                        Throttled[topic].stamp = t
                    else:
                        include = False

            if include:
                outbag.write(topic, msg, t)
