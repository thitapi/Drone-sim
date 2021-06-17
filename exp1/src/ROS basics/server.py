#!/usr/bin/env python

from exp1.srv import Add2int,Add2intResponse
import rospy

def handle_2_no(req):
    rospy.loginfo(rospy.get_caller_id() + "Returning [%s + %s = %s]"%(req.a, req.b, (req.a + req.b)))
    return Add2intResponse(req.a + req.b)

def server():
    rospy.init_node('server')

    # serice name = add_2_int serive type Add2int and All requests are passed to handle_add_two_ints function. 
    # handle_add_two_ints is called with instances of AddTwoIntsRequest and returns instances of AddTwoIntsResponse. 
    s = rospy.Service('add_2_int', Add2int, handle_2_no)
    rospy.loginfo(rospy.get_caller_id() + "Ready to add 2 ints")
    rospy.spin()

if __name__ == "__main__":
    server()
