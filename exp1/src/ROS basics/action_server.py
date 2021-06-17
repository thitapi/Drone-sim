#!/usr/bin/env python
import rospy
import actionlib
import exp1.msg

def execute(g):
    fb = exp1.msg.CountFeedback()
    res = exp1.msg.CountResult()

    success = True
    r=rospy.Rate(g.wait)
    fb.percent = 0
    c=0

    while(c<=g.max):

        # In case of a premption
        if server.is_preempt_requested():
            rospy.loginfo('The goal has been cancelled or preempted')
            server.set_preempted()
            success = False
            break
    
        c = c + 1
        fb.percent= int((c/g.max)*100)
        server.publish_feedback(fb)
        r.sleep()

    if success:
        res.count= c
        rospy.loginfo('Succeeded in counting')
        server.set_succeeded(res)

if __name__ == '__main__':
    rospy.init_node('action_server')

    server = actionlib.SimpleActionServer("Count_act", exp1.msg.CountAction, execute, False)
    server.start()
    rospy.loginfo('Python action server started for counting')

    rospy.spin()    

