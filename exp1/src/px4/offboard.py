#!/usr/bin/env python
import rospy

# 3D point & Stamped Pose msgs
from geometry_msgs.msg import Point, PoseStamped, Twist
# import all mavros messages and services
from mavros_msgs.msg import *
from mavros_msgs.srv import *

# Flight modes class
# Flight modes are activated using ROS services
class fcuModes:
    def __init__(self):
        pass

    def setTakeoff(self):
    	rospy.wait_for_service('mavros/cmd/takeoff')
    	try:
    		takeoffService = rospy.ServiceProxy('mavros/cmd/takeoff', mavros_msgs.srv.CommandTOL)
    		takeoffService(altitude = 3)
    	except rospy.ServiceException as e:
    		rospy.logerr("Service takeoff call failed: %s"%str(e))

    def setArm(self):
        rospy.wait_for_service('mavros/cmd/arming')
        try:
            armService = rospy.ServiceProxy('mavros/cmd/arming', mavros_msgs.srv.CommandBool)
            armService(True)
        except rospy.ServiceException as e:
            rospy.logerr("Service arming call failed: %s"%str(e))

    def setDisarm(self):
        rospy.wait_for_service('mavros/cmd/arming')
        try:
            armService = rospy.ServiceProxy('mavros/cmd/arming', mavros_msgs.srv.CommandBool)
            armService(False)
        except rospy.ServiceException as e:
            rospy.logerr("Service disarming call failed: %s"%str(e))

    def setStabilizedMode(self):
        rospy.wait_for_service('mavros/set_mode')
        try:
            flightModeService = rospy.ServiceProxy('mavros/set_mode', mavros_msgs.srv.SetMode)
            flightModeService(custom_mode='STABILIZED')
        except rospy.ServiceException as e:
            rospy.logerr("service set_mode call failed: %s. Stabilized Mode could not be set."%str(e))

    def setOffboardMode(self):
        rospy.wait_for_service('mavros/set_mode')
        try:
            flightModeService = rospy.ServiceProxy('mavros/set_mode', mavros_msgs.srv.SetMode)
            flightModeService(custom_mode='OFFBOARD')
        except rospy.ServiceException as e:
            rospy.logerr("service set_mode call failed: %s. Offboard Mode could not be set."%str(e))

    def setAltitudeMode(self):
        rospy.wait_for_service('mavros/set_mode')
        try:
            flightModeService = rospy.ServiceProxy('mavros/set_mode', mavros_msgs.srv.SetMode)
            flightModeService(custom_mode='ALTCTL')
        except rospy.ServiceException as e:
            rospy.logerr("service set_mode call failed: %s. Altitude Mode could not be set."%str(e))

    def setPositionMode(self):
        rospy.wait_for_service('mavros/set_mode')
        try:
            flightModeService = rospy.ServiceProxy('mavros/set_mode', mavros_msgs.srv.SetMode)
            flightModeService(custom_mode='POSCTL')
        except rospy.ServiceException as e:
            rospy.logerr("service set_mode call failed: %s. Position Mode could not be set."%str(e))

    def setAutoLandMode(self):
        rospy.wait_for_service('mavros/set_mode')
        try:
            flightModeService = rospy.ServiceProxy('mavros/set_mode', mavros_msgs.srv.SetMode)
            flightModeService(custom_mode='AUTO.LAND')
        except rospy.ServiceException as e:
            rospy.logerr("service set_mode call failed: %s. Autoland Mode could not be set."%str(e))

class Controller:
    # initialization method
    def __init__(self):
        # Drone state
        self.state = State()
        # Instantiate a setpoints message
        self.sp = PositionTarget()
        # init velocity
        self.vel = Twist()
        # set the flag to use position setpoints and yaw angle
        self.sp.type_mask = int('010111111000', 2)
        # LOCAL_NED
        self.sp.coordinate_frame = 1

        # We will fly at a fixed altitude for now
        # Altitude setpoint, [meters]
        self.ALT_SP = 3.0
        # update the setpoint message with the required altitude
        self.sp.position.z = self.ALT_SP
        # Step size for position update
        self.STEP_SIZE = 2.0
		# Fence. We will assume a square fence for now
        self.FENCE_LIMIT = 5.0

        # A Message for the current local position of the drone
        self.local_pos = Point(0.0, 0.0, 3.0)

        # initial values for setpoints
        self.sp.position.x = 0.0
        self.sp.position.y = 0.0

        # speed of the drone is set using MPC_XY_CRUISE parameter in MAVLink
        # using QGroundControl. By default it is 5 m/s.

	# Callbacks

    ## local position callback
    def posCb(self, msg):
        self.local_pos.x = msg.pose.position.x
        self.local_pos.y = msg.pose.position.y
        self.local_pos.z = msg.pose.position.z
        rospy.loginfo("Current position :"+str(self.local_pos))

    ## Drone State callback
    def stateCb(self, msg):
        self.state = msg
        rospy.loginfo("Current state: "+str(self.state))

    ## Update setpoint message
    def updateSp(self):
        self.sp.position.x = self.local_pos.x
        self.sp.position.y = self.local_pos.y

    def x_dir(self):
    	self.sp.position.x = self.local_pos.x + 5
    	self.sp.position.y = self.local_pos.y

    def neg_x_dir(self):
    	self.sp.position.x = self.local_pos.x - 5
    	self.sp.position.y = self.local_pos.y

    def y_dir(self):
    	self.sp.position.x = self.local_pos.x
    	self.sp.position.y = self.local_pos.y + 5

    def neg_y_dir(self):
    	self.sp.position.x = self.local_pos.x
    	self.sp.position.y = self.local_pos.y - 5

    def twistCb(self,data):
        self.vel= data
        rospy.loginfo("Current state: "+str(self.vel))


# Main function
def main():

    # initiate node
    rospy.init_node('offboard_node', anonymous=True)

    # flight mode object
    modes = fcuModes()

    # controller object
    cnt = Controller()

    # ROS loop rate should be > 2Hz
    rate = rospy.Rate(20.0)

    # Subscribe to drone state
    rospy.Subscriber('mavros/state', State, cnt.stateCb)

    # Subscribe to drone's local position
    rospy.Subscriber('mavros/local_position/pose', PoseStamped, cnt.posCb)

    # Subscribe to /cmd_vel for teleoperation
    rospy.Subscriber('/cmd_vel', Twist, cnt.twistCb)

    # Setpoint publisher    
    sp_pub = rospy.Publisher('mavros/setpoint_raw/local', PositionTarget)

    # Setpoint_velocity publisher
    vel_pub = rospy.Publisher('/mavros/setpoint_velocity/cmd_vel_unstamped', Twist)

    # Make sure the drone is armed
    while not cnt.state.armed:
        modes.setArm()
        rate.sleep()

    # set in takeoff mode and takeoff to default altitude (3 m)
    modes.setTakeoff()
    rate.sleep()

    # We need to send few setpoint messages, then activate OFFBOARD mode, to take effect
    k=0
    while k<100:
        sp_pub.publish(cnt.sp)
        rate.sleep()
        k = k + 1

    # activate OFFBOARD mode
    modes.setOffboardMode()

    # ROS main loop
    last_request=rospy.Time.now()
    while not rospy.is_shutdown():
    	cnt.updateSp()
        ''' for testing position stream control
        if rospy.Time.now() - last_request < rospy.Duration(20.0):
            cnt.x_dir()
            rospy.loginfo("^^^^^^Going positive x + 5^^^^^^^") 
        elif rospy.Time.now() - last_request < rospy.Duration(23.0):
            cnt.y_dir() 
            rospy.loginfo("^^^^^^Going positive y + 5^^^^^^^")
        ''' 
    	sp_pub.publish(cnt.sp)
        vel_pub.publish(cnt.vel)
    	rate.sleep()

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass