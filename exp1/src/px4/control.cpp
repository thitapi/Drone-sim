#include <ros/ros.h>
#include <geometry_msgs/PoseStamped.h>

#include <mavros_msgs/CommandBool.h>
#include <mavros_msgs/SetMode.h>
#include <mavros_msgs/State.h>

#include<mavros_msgs/ManualControl.h>

mavros_msgs::State current_state;
void state_cb(const mavros_msgs::State::ConstPtr& msg){
    current_state = *msg;
}

int main(int argc, char **argv)
{
    ros::init(argc, argv, "offb_node");
    ros::NodeHandle n;

    // feedback from the controller
    ros::Subscriber state_sub = n.subscribe<mavros_msgs::State>
            ("mavros/state", 10, state_cb);

    // control command services
    ros::ServiceClient arming_client = n.serviceClient<mavros_msgs::CommandBool>
            ("mavros/cmd/arming");
    ros::ServiceClient set_mode_client = n.serviceClient<mavros_msgs::SetMode>
            ("mavros/set_mode");

    // to give a continuous steam of coordinates for offboard mode
    ros::Publisher local_pos_pub = n.advertise<geometry_msgs::PoseStamped>
            ("mavros/setpoint_position/local", 10);

    //the setpoint publishing rate MUST be faster than 2Hz
    ros::Rate rate(20.0);

    // wait for FCU connection
    while(ros::ok() && !current_state.connected){
        ros::spinOnce();
        rate.sleep();
    }
      
    // Arming 
    while(ros::ok() && !current_state.armed){
        mavros_msgs::CommandBool arm_cmd;
        arm_cmd.request.value = true;
        arming_client.call(arm_cmd);
        if(arm_cmd.response.success)
        {ROS_INFO("Armed"); break;}
        else
        ROS_ERROR("Failed to Arm retrying....");
    }

    mavros_msgs::SetMode man_set_mode;
    geometry_msgs::PoseStamped pose;
    man_set_mode.request.custom_mode = "AUTO.TAKEOFF";
    set_mode_client.call(man_set_mode);
    sleep(2);

    ros::Time last_request = ros::Time::now();
    while(ros::ok() && !current_state.armed)
    {
        if (ros::Time::now() - last_request < ros::Duration(2.0))
        {
            man_set_mode.request.custom_mode = "ALTITUDE";
            set_mode_client.call(man_set_mode); 
            sleep(5);
        }
        else  
        {
            man_set_mode.request.custom_mode = "OFFBOARD";
            set_mode_client.call(man_set_mode);
            while(!man_set_mode.response.mode_sent)
            {
                ROS_ERROR("Failed to set mode retrying....");
                man_set_mode.request.custom_mode = "OFFBOARD";
                set_mode_client.call(man_set_mode);
            }
            ROS_INFO("Mode set to off board");

            if (ros::Time::now() - last_request < ros::Duration(20.0))
            {
                pose.pose.position.x = 0;
                pose.pose.position.y = 0;
                pose.pose.position.z = 10;
                local_pos_pub.publish(pose);
                ROS_INFO("^^^^^^at (0,0,10)^^^^^^^"); 
            }
            else if (ros::Time::now() - last_request < ros::Duration(23.0))
            {
                pose.pose.position.x = 0;
                pose.pose.position.y = 2;
                pose.pose.position.z = 10;
                local_pos_pub.publish(pose); 
                ROS_INFO("^^^^^^at (0,2,10)^^^^^^^"); 
            }
            else if (ros::Time::now() - last_request < ros::Duration(26.0))
            {
                pose.pose.position.x = 0;
                pose.pose.position.y = -3;
                pose.pose.position.z = 10;
                local_pos_pub.publish(pose);
                ROS_INFO("^^^^^^at (0,-3,10)^^^^^^^");  
            }

            else{
                man_set_mode.request.custom_mode = "AUTO.LAND";
                set_mode_client.call(man_set_mode); 
                break;
            }
            
        }
    }
}



