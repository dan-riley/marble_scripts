import sys
import os
import re

if __name__ == '__main__':
    # Usage: python parse_rosout.py inputfolder outputfolder
    # By default will look in ~/.ros/log/latest and output will be the current folder

    home = os.path.expanduser("~")

    if len(sys.argv) > 1:
        inputfolder = sys.argv[1]
    else:
        inputfolder = home + "/.ros/log/latest"

    if len(sys.argv) > 2:
        outputfolder = sys.argv[2]
    else:
        outputfolder = os.getcwd()

    print('looking in ' + inputfolder + ' and writing to ' + outputfolder)
    nodes = {}
    files = []
    for filename in os.listdir(inputfolder):
        if "rosout.log" in filename and "swp" not in filename:
            files.append(filename)

    # We want to go through the rosout logs in reverse order so the timestamps are sequential
    files.sort(reverse=True)
    for filename in files:
        print('processing ' + filename)
        with open(os.path.join(inputfolder, filename)) as fp:
            line = fp.readline()
            lastnode = []
            while line:
                # Regular node log lines include [topics] [garbage] so match that
                regex = re.compile('\[.*?\] \[.*?\]')
                if regex.search(line):
                    # Get the node name and then rebuild the line
                    nl = regex.sub('', line).split(' ')
                    node = nl.pop(2).replace('/', '_')[1:]
                    nl = ' '.join(nl)
                    # Add to the node
                    if node not in nodes:
                        nodes[node] = [nl]
                    else:
                        nodes[node].append(nl)

                    lastnode = nodes[node]
                else:
                    # Add continuation lines to the previous node line
                    lastnode.append(line)

                line = fp.readline()

    # Write each file
    for node in nodes:
        with open(os.path.join(outputfolder, node + '.log'), 'w') as fp:
            fp.writelines(nodes[node])
