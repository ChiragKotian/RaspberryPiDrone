#!/usr/bin/env python3

import rospy
import numpy as np

from geometry_msgs.msg import PoseStamped, Quaternion, Vector3
from mavros_msgs.msg import State, AttitudeTarget
from mavros_msgs.srv import CommandBool, CommandBoolRequest, SetMode, SetModeRequest
from drone_pkg.msg import human_inputs
from drone_pkg.msg import quad_states
from tf.transformations import quaternion_from_euler
import time

global current_state1, current_state2
current_state1 = State()
current_state2 = State()

global Channels1, Channels2
Channels1 = [1500,1500,1500,1500,1500,1500,1500,1500,0,0]
Channels2 = [1500,1500,1500,1500,1500,1500,1500,1500,0,0]
# channel - 1 = roll angle
# channel - 2 = pitch angle
# channel - 3 = throttle angle
# channel - 4 = yaw angle

# channel - 5 = Mode switch [Loiter, loiter, stabilize]
# channel - 6 = empty
# channel - 7 = empty
# channel - 8 = toggle offboard

global des_ph1, des_th1, des_ps1, des_throttle1
des_ph1 = 0.0
des_th1 = 0.0
des_ps1 = 0.0
des_throttle1 = 0.0

global des_ph2, des_th2, des_ps2, des_throttle2
des_ph2 = 0.0
des_th2 = 0.0
des_ps2 = 0.0
des_throttle2 = 0.0

global quad_state1, collision, quad_state2
quad_state1 = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
quad_state2 = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]

raspmode = "OFFBOARD"

collision = False

def get_quaternion_from_euler(roll, pitch, yaw):

    qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
    qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
    qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
    qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
    
    return [qx, qy, qz, qw]


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
    quad_state1[5]=data.quad_ps
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
    quad_state2[5]=data.quad_ps
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
    scale1 = ((Channels1[3]-1500.0)/500.0)*5.0*5  #5.0 determines max speed in degrees/sec and set 10.0 as per the spped at which your script is running at
    des_ps_deg1= (quad_state1[5])+scale1

    if(des_ps_deg1>=360.0):
        des_ps_deg1= des_ps_deg1-360
    elif(des_ps_deg1<0):
        des_ps_deg1= des_ps_deg1+360

    des_ps1= des_ps_deg1* 3.14159265359 / 180.0

    global quad_state2, des_ps2
    scale2 = ((Channels2[3]-1500.0)/500.0)*5.0*5  #5.0 determines max speed in degrees/sec and set 10.0 as per the spped at which your script is running at
    des_ps_deg2= (quad_state2[5])+scale2

    if(des_ps_deg2>=360.0):
        des_ps_deg2= des_ps_deg2-360
    elif(des_ps_deg2<0):
        des_ps_deg2= des_ps_deg2+360

    des_ps2= des_ps_deg2* 3.14159265359 / 180.0



if __name__ == "__main__":

    rospy.init_node("offb_node_py")

    state_sub1 = rospy.Subscriber("/drone1/mavros/state", State, callback = state_cb1)
    state_sub2= rospy.Subscriber("/drone2/mavros/state", State, callback = state_cb2)

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

    att_pub1 = rospy.Publisher("/drone1/mavros/setpoint_raw/attitude", AttitudeTarget, queue_size=1)
    att_pub2 = rospy.Publisher("/drone2/mavros/setpoint_raw/attitude", AttitudeTarget, queue_size=1)

    # Setpoint publishing MUST be faster than 2Hz
    rate = rospy.Rate(100) # 100 Hz

    # Wait for Flight Controller connection
    while(not rospy.is_shutdown() and not current_state1.connected):
        rate.sleep()
    
    while(not rospy.is_shutdown() and not current_state2.connected):
        rate.sleep()

    att1 = AttitudeTarget()
    att2 = AttitudeTarget()

    while(not rospy.is_shutdown() ):

        # To get the desired values of the attitude and throttle
        des_ph1 = ((Channels1[0] - 1500.0) / 500.0) * 45.0 * 3.14159265359 / 180.0
        des_th1 = ((Channels1[1] - 1500.0) / 500.0) * 45.0 * 3.14159265359 / 180.0
        des_ph2 = ((Channels2[0] - 1500.0) / 500.0) * 45.0 * 3.14159265359 / 180.0
        des_th2 = ((Channels2[1] - 1500.0) / 500.0) * 45.0 * 3.14159265359 / 180.0
        determine_yaw() 
        des_throttle1 = (Channels1[2] - 1000.0) / 1000.0
        des_throttle2 = (Channels2[2] - 1000.0) / 1000.0

        print(" des_ph1 -> " + str(des_ph1) + " des_th1 -> " + str(des_th1)+ " des_ps1 -> " + str(des_ps1) + " des_throttle1 -> " + str(des_throttle1))
        print(" des_ph2 -> " + str(des_ph2) + " des_th2 -> " + str(des_th2)+ " des_ps2 -> " + str(des_ps2) + " des_throttle2 -> " + str(des_throttle2))

        #  Assigning the values to the topics
        att1.orientation = Quaternion(*quaternion_from_euler(des_ph1,des_th1,des_ps1)) # The inputs are in radians
        att1.thrust = des_throttle1
        att1.type_mask = 7
        att2.orientation = Quaternion(*quaternion_from_euler(des_ph2,des_th2,des_ps2)) # The inputs are in radians
        att2.thrust = des_throttle2
        att2.type_mask = 7
        while(collision):
            time.sleep(0.1)
        # finally publish the data
        att_pub1.publish(att1)
        att_pub2.publish(att2)
        rate.sleep()
