import sys
import rospy
import rosbag
import csv

if __name__ == '__main__':
    inputfile = sys.argv[1]
    vehicle = sys.argv[2]
    prefix = ''
    if len(sys.argv) > 2:
        prefix = sys.argv[3] + '/'
    bobcat_topic = '/' + prefix + vehicle + '/bobcat_status'
    start = None
    startLine = None

    with open(vehicle + '_bobcat.csv', 'wb') as csvfile:
        print('creating BOBCAT status for ' + vehicle)
        wr = csv.writer(csvfile)
        for topic, msg, t in rosbag.Bag(inputfile).read_messages():
            if not start:
                start = t


            if topic == bobcat_topic:
                if not startLine:
                    startLine = ['Time', 'ExecBehavior', 'ExecScore']
                    for monitor in msg.monitors:
                        startLine.append(monitor.name)
                    for objective in msg.objectives:
                        startLine.append(objective.name)
                    for behavior in msg.behaviors:
                        startLine.append(behavior.name)
                    wr.writerow(startLine)

                line = [(t-start).secs, msg.execBehavior]
                for behavior in msg.behaviors:
                    if behavior.name == msg.execBehavior:
                        line.append(round(behavior.score, 1))
                        break
                # print(line)
                for monitor in msg.monitors:
                    line.append(int(monitor.status))
                for objective in msg.objectives:
                    line.append(round(objective.weight, 1))
                for behavior in msg.behaviors:
                    line.append(round(behavior.score, 1))
                wr.writerow(line)
