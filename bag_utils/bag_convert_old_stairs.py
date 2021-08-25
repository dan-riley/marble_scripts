import sys
import rosbag

if __name__ == '__main__':
    inputfile = sys.argv[1]
    if len(sys.argv) == 3:
        outputfile = sys.argv[2]
    else:
        outputfile = inputfile[:-4] + '-converted.bag'

    with rosbag.Bag(outputfile, 'w') as outbag:
        for topic, msg, t in rosbag.Bag(inputfile).read_messages():
            if 'merged_map' in topic:
                msg.id = msg.id.replace('RoughOcTree-', 'RoughOcTree-S-')
            outbag.write(topic, msg, t)
