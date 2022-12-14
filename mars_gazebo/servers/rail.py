#!/usr/bin/env python3

import rospy
from gazebo_msgs.msg import *
from geometry_msgs.msg import *

COMP="rail::head"

class Wrap:
    def __init__(self):
        rospy.wait_for_service("/gazebo/set_link_state")
        self.pub = rospy.Publisher("/gazebo/set_link_state", LinkState, queue_size=60)
        self.sub = rospy.Subscriber("/gazebo/link_states", LinkStates, self.cb)

    def cb(self, msg: LinkStates):
        names = msg.name
        names: list
        idx = names.index(COMP)

        self.pose = msg.pose[idx]
        self.twist = msg.twist[idx]

    def step(self, dist):
        pose = self.pose
        twist = self.twist

        pose.position.x += dist
            
        self.pub.publish(
            LinkState(
                link_name=COMP,
                pose=pose,
                twist=twist,
                # reference_frame
            )
        )

rospy.init_node("Teleop")
w = Wrap()
rospy.loginfo("Ready")
while not rospy.is_shutdown():
    i = input(">")
    d = float(i)

    w.step(d)