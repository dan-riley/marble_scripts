import sys
import rospy
import rosbag
from marble_mapping.msg import OctomapNeighbors
from marble_mapping.msg import OctomapArray

if __name__ == '__main__':
    # Usage: python map_to_neighbor.py inputfile.bag agents topic outputfile.bag
    # agents = X1,X2, etc
    # topic = octomap_binary

    inputfile = sys.argv[1]
    if len(sys.argv) > 2:
        agents = sys.argv[2].split(',')
    else:
        agents = ['X1','X2']

    if len(sys.argv) > 3:
        intopic = sys.argv[3]
    else:
        intopic = 'octomap_binary'

    if len(sys.argv) == 5:
        outputfile = sys.argv[4]
    else:
        outputfile = inputfile[:-4] + '-map.bag'

    with rosbag.Bag(outputfile, 'w') as outbag:
        for topic, msg, t in rosbag.Bag(inputfile).read_messages():
            for agent in agents:
                if '/' + agent + '/' + intopic in topic:
                    diff = OctomapArray()
                    diff.owner = agent
                    diff.num_octomaps = 1
                    diff.octomaps.append(msg)

                    nmsg = OctomapNeighbors()
                    nmsg.num_neighbors = 1
                    nmsg.neighbors.append(diff)
                    for agentw in agents:
                        outTopic = '/' + agentw + '/neighbor_maps'
                        outbag.write(outTopic, nmsg, t)
