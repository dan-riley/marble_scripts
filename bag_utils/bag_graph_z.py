import sys
import rospy
import rosbag
from matplotlib import pyplot as plt

if __name__ == '__main__':
    # Usage: python bag_graph_z.py inputfile.bag outputfile.png
    # Topic to find the z data
    odomTopic = '/A01/odometry'
    # Vertical limit to calculate time below
    zlim = 4.0

    inputfile = sys.argv[1]
    if len(sys.argv) == 3:
        outputfile = sys.argv[2]
    else:
        outputfile = inputfile[:-3] + 'png'

    z = []
    time = []
    started = False
    starttime = 0
    endtime = 0
    cumetime = 0
    for topic, msg, t in rosbag.Bag(inputfile).read_messages():
        if topic == odomTopic:
            zpos = msg.pose.pose.position.z
            curtime = t.secs + 1e-9 * t.nsecs
            # Save to the lists for plotting
            z.append(zpos)
            time.append(curtime)
            # Check if we've crossed the threshold yet
            if not started and zpos > zlim:
                started = True
            elif not started:
                continue

            # Once we've crossed the threshold once, start looking for dips below
            if zpos < zlim:
                if not starttime:
                    starttime = curtime
                else:
                    endtime = curtime

                if zpos < 1.0:
                    # Once we hit one meter get the last time, and then stop
                    # Could be an issue if we fly below one meter but for current tests not an issue
                    cumetime += endtime - starttime
                    starttime = 0
                    endtime = 0
                    started = False
            else:
                if endtime > starttime:
                    cumetime += endtime - starttime
                    starttime = 0
                    endtime = 0

    if endtime > starttime:
        cumetime += endtime - starttime

    print "Total time below", zlim, "meters was", cumetime, "seconds"
    plt.plot(time, z)
    plt.title(inputfile[:-4])
    plt.axhline(y=4.0, color='r', linestyle='-')
    # plt.show()
    plt.savefig(outputfile)
