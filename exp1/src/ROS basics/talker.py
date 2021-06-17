#!/usr/bin/env python
import rospy
from std_msgs.msg import String

def talker():
    '''declares that your node is publishing to the chatter topic using the message type String. 
    String here is actually the class std_msgs.msg.String.''' 
    pub = rospy.Publisher('chatter', String)

    ''' it tells rospy the name of your node -- until rospy has this information, it cannot start communicating with the ROS Master. 
    In this case, your node will take on the name talker.  
    anonymous = True ensures that your node has a unique name by adding random numbers to the end of NAME.'''
    rospy.init_node('talker')

    '''This line creates a Rate object rate.
     With the help of its method sleep(), it offers a convenient way for looping at the desired rate. 
     With its argument of 10, we should expect to go through the loop 10 times per second (as long as our processing time does not exceed 1/10th of a second!)'''
    rate = rospy.Rate(10) #10Hz


    while not rospy.is_shutdown():
        hello_sir = "hello world %s" % rospy.get_time()

        '''This loop also calls rospy.loginfo(str), which performs triple-duty: 
        the messages get printed to screen, 
        it gets written to the Node's log file, 
        and it gets written to rosout. rosout is a handy tool for debugging: 
        you can pull up messages using rqt_console instead of having to find the console window with your Node's output. '''
        rospy.loginfo(hello_sir)

        pub.publish(hello_sir)
        rate.sleep()
    
if __name__== '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass