import sys
import rospy
import rosbag

if __name__ == '__main__':
    # Usage: python bag_trim.py inputfile.bag outputfile.bag

    # Start and end times for the output bag.  Check the actual times in rosbag play ("Bag Time")
    # Times in secs, nsecs
    starttime = rospy.Time(73, 0)
    endtime = rospy.Time(84, 0)

    inputfile = sys.argv[1]
    if len(sys.argv) == 3:
        outputfile = sys.argv[2]
    else:
        outputfile = 'output.bag'

    with rosbag.Bag(outputfile, 'w') as outbag:
        for topic, msg, t in rosbag.Bag(inputfile).read_messages():
            if t >= starttime and t <= endtime:
                outbag.write(topic, msg, t)
