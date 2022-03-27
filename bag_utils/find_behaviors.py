import sys
import rospy
import rosbag

if __name__ == '__main__':
    inputfile = sys.argv[1]
    vehicle = sys.argv[2]
    bobcat_topic = '/' + vehicle + '/bobcat_status'
    behavior = 'Explore'
    start = None

    for topic, msg, t in rosbag.Bag(inputfile).read_messages():
        if not start:
            start = t

        if topic == bobcat_topic:
            if msg.execBehavior != behavior:
                behavior = msg.execBehavior
                objectives = []
                for objective in msg.objectives:
                    if objective.weight and objective.name != 'Explore':
                        objectives.append(objective.name)
                print((t-start).secs, behavior, objectives)
