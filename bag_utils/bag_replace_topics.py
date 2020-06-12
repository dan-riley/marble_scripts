import rosbag
with rosbag.Bag('output.bag', 'w') as outbag:
    for topic, msg, t in rosbag.Bag('darpa_test2.bag').read_messages():
        msg.id = msg.id.replace('X', 'H0')
        if msg.neighbors:
            msg.neighbors[0].id = msg.neighbors[0].id.replace('X', 'H0')
        outbag.write(topic, msg, t)
