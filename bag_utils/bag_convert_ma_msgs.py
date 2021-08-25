import sys
import rospy
import rosbag
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped
from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray
from marble_multi_agent.msg import AgentMsg

def buildArtifacts(martifacts, artifacts):
    i = len(martifacts.markers)
    for artifact in artifacts.artifacts:
        found = False
        for marker in martifacts.markers:
            if marker.pose.position == artifact.position:
                found = True

        if not found:
            martifact = Marker()
            martifact.header.frame_id = 'world'
            martifact.id = i
            martifact.type = martifact.TEXT_VIEW_FACING
            martifact.action = martifact.ADD

            martifact.scale.x = 1.0
            martifact.scale.y = 1.0
            martifact.scale.z = 1.0

            martifact.color.a = 1.0
            martifact.color.r = 1.0
            martifact.color.g = 1.0
            martifact.color.b = 1.0
            martifact.pose.position = artifact.position
            martifact.text = artifact.obj_class

            martifacts.markers.append(martifact)
            i = i + 1

    return martifacts

def decompressPath(cpath):
    path = Path()
    path.header.stamp = rospy.Time()
    path.header.frame_id = "world"
    i = 0
    while i < len(cpath):
        pose = PoseStamped()
        pose.header.frame_id = "world"
        pose.header.stamp = rospy.Time()
        pose.pose.position.x = 0.1 * cpath[i]
        i += 1
        pose.pose.position.y = 0.1 * cpath[i]
        i += 1
        pose.pose.position.z = 0.1 * cpath[i]
        i += 1
        path.poses.append(pose)

    return path

if __name__ == '__main__':
    # Usage: python bag_convert_ma_msgs.py inputfile.bag outputfile.bag

    inputfile = sys.argv[1]
    if len(sys.argv) == 3:
        outputfile = sys.argv[2]
    else:
        outputfile = inputfile[:-4] + '-ma.bag'

    martifacts = MarkerArray()
    mbeacon = Marker()
    mbeacon.header.frame_id = 'world'
    mbeacon.type = mbeacon.CUBE_LIST
    mbeacon.action = mbeacon.ADD
    mbeacon.scale.x = 1.0
    mbeacon.scale.y = 1.0
    mbeacon.scale.z = 1.0
    mbeacon.color.a = 1.0
    mbeacon.color.r = 1.0
    mbeacon.color.g = 1.0
    mbeacon.color.b = 1.0

    with rosbag.Bag(outputfile, 'w') as outbag:
        for topic, msg, t in rosbag.Bag(inputfile).read_messages():
            outbag.write(topic, msg, t)
            if 'blacklist' in topic:
                tid = topic.split('/')[2]
                blTopic = '/' + tid + '/blacklist'
                outbag.write(blTopic, msg, t)

            if 'ma_data' in topic:
                odomTopic = '/' + msg.id + '/ma_pose'
                odomMsg = msg.odometry
                outbag.write(odomTopic, odomMsg, t)

                # Old uncompressed message type
                # goalTopic = '/' + msg.id + '/ma_goal'
                # goalMsg = msg.goal.pose
                # outbag.write(goalTopic, goalMsg, t)
                #
                # pathTopic = '/' + msg.id + '/ma_goal_path'
                # pathMsg = msg.goal.path
                # outbag.write(pathTopic, pathMsg, t)

                # New compressed message type
                pathTopic = '/' + msg.id + '/ma_goal_path'
                pathMsg = decompressPath(msg.goal.path)
                outbag.write(pathTopic, pathMsg, t)

                goalTopic = '/' + msg.id + '/ma_goal'
                goalMsg = PoseStamped()
                if len(pathMsg.poses):
                    goalMsg = pathMsg.poses[-1]
                outbag.write(goalTopic, goalMsg, t)

                mbeacon.points = []
                for beacon in msg.commBeacons.data:
                    if beacon.active:
                        mbeacon.points.append(beacon.pos)

                beaconTopic = '/Base/mbeacons'
                outbag.write(beaconTopic, mbeacon, t)

                artifactTopic = '/Base/martifacts'
                outbag.write(artifactTopic, buildArtifacts(martifacts, msg.newArtifacts), t)
