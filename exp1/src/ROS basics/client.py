#!/usr/bin/env python

from exp1.srv import *
import rospy
import sys

def client(x, y):
    rospy.wait_for_service('add_2_int')
    try:
        add = rospy.ServiceProxy('add_2_int', Add2int)
        resp1 = add(x,y)
        return resp1.sum
    except rospy.ServiceException as e:
        rospy.logerr(rospy.get_caller_id() + "Service call failed: %s"%e)

def usage():
    return "%s [x,y]"%sys.argv[0]

if __name__ == "__main__":
    if len(sys.argv) == 3:
        x=int(sys.argv[1]) 
        y=int(sys.argv[2])
    else:
        rospy.loginfo(rospy.get_caller_id() + usage())    
    rospy.loginfo(rospy.get_caller_id() + "Requesting %s+%s"%(x,y))
    rospy.loginfo(rospy.get_caller_id() + "%s + %s = %s"%(x,y,client(x,y)))
    sys.exit(0)
        