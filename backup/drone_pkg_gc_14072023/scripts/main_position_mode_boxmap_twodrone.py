#!/usr/bin/env python3

import rospy
import time
import numpy as np

from geometry_msgs.msg import PoseStamped, Quaternion, Vector3
from mavros_msgs.msg import State
from mavros_msgs.srv import CommandBool, CommandBoolRequest, SetMode, SetModeRequest
from drone_pkg.msg import human_inputs
from drone_pkg.msg import quad_states
from tf.transformations import quaternion_from_euler

global current_state1
current_state1 = State()
global Channels1
Channels1 = [1500,1500,1500,1500,1500,1500,1500,1500,0,0]
global current_state2
current_state2 = State()
global Channels2
Channels2 = [1500,1500,1500,1500,1500,1500,1500,1500,0,0]
# channel - 1 = roll angle
# channel - 2 = pitch angle
# channel - 3 = throttle angle
# channel - 4 = yaw angle

# channel - 5 = Mode switch [Loiter, loiter, stabilize]
# channel - 6 = empty
# channel - 7 = empty
# channel - 8 = toggle offboard

global des_ph1, des_th1, des_ps1 #in radians
des_ph1 = 0.0
des_th1 = 0.0
des_ps1 = 0.0

global des_ph2, des_th2, des_ps2 #in radians
des_ph2 = 0.0
des_th2 = 0.0
des_ps2 = 0.0

global quad_state1
quad_state1 = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
global quad_state2
quad_state2 = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]

global coordinates1, collision
coordinates1=[0,0,0] #(x,y,z)(forward,right,down)
global coordinates2
coordinates2=[0,0,0] #(x,y,z)(forward,right,down)

global boxlength #(equals 1/2 the total length,width and height)
boxlength = 2.0

offsets1 = [0.0,0.0,0]
offsets2 = [0.0,0.0,0]

raspmode = "OFFBOARD"
collision= False

def state_cb1(msg):
    global current_state1
    current_state1 = msg

def state_cb2(msg):
    global current_state2
    current_state2 = msg

def channels_callback1(data):
    global Channels1
    Channels1[0]=data.channel1
    Channels1[1]=data.channel2
    Channels1[2]=data.channel3
    Channels1[3]=data.channel4
    Channels1[4]=data.channel5
    Channels1[5]=data.channel6
    Channels1[6]=data.channel7
    Channels1[7]=data.channel8

def channels_callback2(data):
    global Channels2
    Channels2[0]=data.channel1
    Channels2[1]=data.channel2
    Channels2[2]=data.channel3
    Channels2[3]=data.channel4
    Channels2[4]=data.channel5
    Channels2[5]=data.channel6
    Channels2[6]=data.channel7
    Channels2[7]=data.channel8

def quad_states_callback1(data):
    global quad_state1, collision
    quad_state1[0]=data.quad_x
    quad_state1[1]=data.quad_y
    quad_state1[2]=data.quad_z
    quad_state1[3]=data.quad_ph
    quad_state1[4]=data.quad_th
    quad_state1[5]=data.quad_ps   #yaw
    quad_state1[6]=data.quad_x_dot
    quad_state1[7]=data.quad_y_dot
    quad_state1[8]=data.quad_z_dot
    quad_state1[9]=data.quad_ph_dot
    quad_state1[10]=data.quad_th_dot
    quad_state1[11]=data.quad_ps_dot
    quad_state1[12]=data.quad_x_dot_dot
    quad_state1[13]=data.quad_y_dot_dot
    quad_state1[14]=data.quad_z_dot_dot
    collision = data.collision

def quad_states_callback2(data):
    global quad_state2, collision
    quad_state2[0]=data.quad_x
    quad_state2[1]=data.quad_y
    quad_state2[2]=data.quad_z
    quad_state2[3]=data.quad_ph
    quad_state2[4]=data.quad_th
    quad_state2[5]=data.quad_ps   #yaw
    quad_state2[6]=data.quad_x_dot
    quad_state2[7]=data.quad_y_dot
    quad_state2[8]=data.quad_z_dot
    quad_state2[9]=data.quad_ph_dot
    quad_state2[10]=data.quad_th_dot
    quad_state2[11]=data.quad_ps_dot
    quad_state2[12]=data.quad_x_dot_dot
    quad_state2[13]=data.quad_y_dot_dot
    quad_state2[14]=data.quad_z_dot_dot
    collision = data.collision

def determine_yaw():
    global quad_state1, des_ps1
    scale1 = ((Channels1[3]-1500.0)/500.0)*10.0  #5.0 determines max speed in degrees/sec and set 10.0 as per the spped at which your script is running at
    des_ps_deg1= (quad_state1[5])+scale1

    if(des_ps_deg1>=360.0):
        des_ps_deg1= des_ps_deg1-360
    elif(des_ps_deg1<0):
        des_ps_deg1= des_ps_deg1+360

    des_ps1= des_ps_deg1* 3.14159265359 / 180.0

    global quad_state2, des_ps2
    scale2 = ((Channels2[3]-1500.0)/500.0)*10.0  #5.0 determines max speed in degrees/sec and set 10.0 as per the spped at which your script is running at
    des_ps_deg2= (quad_state2[5])+scale2

    if(des_ps_deg2>=360.0):
        des_ps_deg2= des_ps_deg2-360
    elif(des_ps_deg2<0):
        des_ps_deg2= des_ps_deg2+360

    des_ps2= des_ps_deg2* 3.14159265359 / 180.0



if __name__ == "__main__":

    rospy.init_node("offb_node_py")

    state_sub1 = rospy.Subscriber("/drone1/mavros/state", State, callback = state_cb1)
    state_sub2 = rospy.Subscriber("/drone2/mavros/state", State, callback = state_cb2)

    rospy.Subscriber("/drone1/quad/quad_states", quad_states, quad_states_callback1)
    rospy.Subscriber("/drone1/quad/human_inputs", human_inputs, channels_callback1)
    rospy.Subscriber("/drone2/quad/quad_states", quad_states, quad_states_callback2)
    rospy.Subscriber("/drone2/quad/human_inputs", human_inputs, channels_callback2)

    rospy.wait_for_service("/drone1/mavros/cmd/arming")
    arming_client1 = rospy.ServiceProxy("/drone1/mavros/cmd/arming", CommandBool)
    rospy.wait_for_service("/drone2/mavros/cmd/arming")
    arming_client2 = rospy.ServiceProxy("/drone2/mavros/cmd/arming", CommandBool)

    rospy.wait_for_service("/drone1/mavros/set_mode")
    set_mode_client1 = rospy.ServiceProxy("/drone1/mavros/set_mode", SetMode)
    rospy.wait_for_service("/drone2/mavros/set_mode")
    set_mode_client2 = rospy.ServiceProxy("/drone2/mavros/set_mode", SetMode)

    local_pos_pub1 = rospy.Publisher("/drone1/mavros/setpoint_position/local", PoseStamped, queue_size=10)
    local_pos_pub2 = rospy.Publisher("/drone2/mavros/setpoint_position/local", PoseStamped, queue_size=10)

    # Setpoint publishing MUST be faster than 2Hz
    rate = rospy.Rate(100) # 100 Hz

    # Wait for Flight Controller connection
    while(not rospy.is_shutdown() and not current_state1.connected):
        rate.sleep()
    while(not rospy.is_shutdown() and not current_state2.connected):
        rate.sleep()

    pos1 = PoseStamped()
    pos2 = PoseStamped()

    while(not rospy.is_shutdown() ):
        determine_yaw()

        coordinates1[0]= ((Channels1[1] - 1500.0)/500.0)* boxlength*-1
        coordinates1[1]= ((Channels1[0] - 1500.0)/500.0)* boxlength*-1
        coordinates1[2]= ((Channels1[2]-1000.0)/500.0)* boxlength
        pos1.pose.position.x = coordinates1[0]+offsets1[0]
        pos1.pose.position.y = coordinates1[1]+offsets1[1]
        pos1.pose.position.z = coordinates1[2]+offsets1[2]

        coordinates2[0]= ((Channels2[1] - 1500.0)/500.0)* boxlength*-1
        coordinates2[1]= ((Channels2[0] - 1500.0)/500.0)* boxlength*-1
        coordinates2[2]= ((Channels2[2]-1000.0)/500.0)* boxlength
        pos2.pose.position.x = coordinates2[0]+offsets2[0]
        pos2.pose.position.y = coordinates2[1]+offsets2[1]
        pos2.pose.position.z = coordinates2[2]+offsets2[2]
       
        pos1.pose.orientation = Quaternion(*quaternion_from_euler(des_ph1,des_th1,des_ps1)) # The inputs are in radians
        print(" x1 -> " + str(pos1.pose.position.x) + " y1 -> " + str(pos1.pose.position.y) + " des_throttle1 -> " + str(pos1.pose.position.z) + " yaw1 -> "+ str(des_ps1*180/3.14159265359))
        pos2.pose.orientation = Quaternion(*quaternion_from_euler(des_ph2,des_th2,des_ps2)) # The inputs are in radians
        print(" x2 -> " + str(pos2.pose.position.x) + " y2 -> " + str(pos2.pose.position.y) + " des_throttle2 -> " + str(pos2.pose.position.z) + " yaw2 -> "+ str(des_ps2*180/3.14159265359))
        #  Assigning the values to the topics
        # finally publish the data
        while(collision):
            time.sleep(0.1)
        local_pos_pub1.publish(pos1)
        local_pos_pub2.publish(pos2)
        rate.sleep()
