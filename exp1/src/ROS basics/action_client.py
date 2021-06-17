#!/usr/bin/env python
import rospy
import actionlib
import exp1.msg
from actionlib_msgs.msg import GoalStatus

def feedback_callb(fb):
    rospy.loginfo("percenage completed %s"%fb.percent)

def count(n,r):
    rate=rospy.Rate(1)
    count =0

    g= exp1.msg.CountGoal()
    g.max=n
    g.wait=r
#wait for ther action server
    client.wait_for_server()

    client.send_goal(g, feedback_cb=feedback_callb)
# Get the state of the goal. Possible states are PENDING, ACTIVE, RECALLED, REJECTED, PREEMPTED, ABORTED, SUCCEEDED, LOST.    
    goal_state= client.get_state()

    while not (goal_state == GoalStatus.PREEMPTED or goal_state == GoalStatus.SUCCEEDED):
        if count>10:
            rospy.loginfo("Timed out!")
            client.cancel_goal()
            break

        goal_state= client.get_state()
        count += 1
        rate.sleep()

    rate.sleep()
    goal_state = client.get_state()

    if goal_state == GoalStatus.SUCCEEDED:
        rospy.loginfo("Action completed in Time: result = %d", client.get_result().count)

if __name__ == "__main__":
    rospy.init_node('action_client')
# action name and action type
    client = actionlib.SimpleActionClient("Count_act", exp1.msg.CountAction)

    count(5,10)
