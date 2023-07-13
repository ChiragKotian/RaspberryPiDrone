# make a ros message storing collision warning and if collision eminent then let anti_collision publish data

#this code is for 2 drones

#!/usr/bin/env python3

import rospy
from drone_pkg.msg import quad_states
from geopy import distance
from geometry_msgs.msg import PoseStamped
from mavros_msgs.msg import State

global collision_1_2, avoided, drone_1, drone_2, altitude_1, altitude_2, des_coordinates_1, des_coordinates_2, coordinates_1, coordinates_2, dis_to_trig, separation_push, altitude_local1, altitude_local2
collision_1_2 = False
avoided = False

altitude_local1=0.0
altitude_local2=0.0

drone_1 = [0.0,0.0] #latitude, longitude
altitude_1 = 10.0  #should be greater than separation_push
drone_2 = [0.0,0.0] #latitude, longitude
altitude_2 = 0.0

separation_push = 3.0 #distance to push drones apart in altitude case of collision

dis_to_trig = 2.0  #distance to trigger anticollision

des_coordinates_1=[0.0,0.0,0.0,0.0]
des_coordinates_2=[0.0,0.0,0.0,0.0]

coordinates_1=[0.0,0.0,0.0,0.0]
coordinates_2=[0.0,0.0,0.0,0.0]



def check_collision():
    global collision_1_2, avoided, drone_1, drone_2, altitude_1, altitude_2, dis_to_trig
    if(pow(distance.distance(drone_1,drone_2).m,2)+pow(altitude_1-altitude_2,2)<=pow(dis_to_trig,2)):
        collision_1_2 = True
        print("collision detected")

    elif(pow(distance.distance(drone_1,drone_2).m,2)+pow(altitude_1-altitude_2,2)>pow(dis_to_trig,2) and avoided):
        collision_1_2 = False
        print("collision avoided")
        avoided = False

    else:
        collision_1_2 = False


def avoid_collision():
    global des_coordinates_1, des_coordinates_2, separation_push, avoided
    if(des_coordinates_1[2]<=separation_push or des_coordinates_2[2]<=separation_push):
        if(des_coordinates_1[2]>des_coordinates_2[2]):
            des_coordinates_1[2] = des_coordinates_1[2] + separation_push
        else:
            des_coordinates_2[2] = des_coordinates_2[2] + separation_push

    else:
        des_coordinates_1[2] = des_coordinates_1[2] + (separation_push*0.5)
        des_coordinates_2[2] = des_coordinates_2[2] - (separation_push*0.5)

    avoided = True


def callback_drone1(data):
    global drone_1, altitude_1, altitude_local1, coordinates_1
    drone_1 = [data.quad_latitude, data.quad_longitude]
    altitude_1 = data.quad_altitude
    coordinates_1 = [data.quad_x, data.quad_y, data.quad_z, data.quad_ps]


def callback_drone2(data):
    global drone_2, altitude_2, altitude_local2, coordinates_2
    drone_2 = [data.quad_latitude, data.quad_longitude]
    altitude_2 = data.quad_altitude
    coordinates_2 = [data.quad_x, data.quad_y, data.quad_z, data.quad_ps]


def state_cb(msg):
    global current_state
    current_state = msg


if __name__ == "__main__":

    rospy.init_node("anti_collision")

    state_sub = rospy.Subscriber("/drone1/mavros/state", State, callback = state_cb)    #incase we need some data

    rospy.Subscriber("/drone1/quad/quad_states", quad_states, callback_drone1)
    rospy.Subscriber("/drone2/quad/quad_states", quad_states, callback_drone2)

    local_pos_pub_1 = rospy.Publisher("/drone1/mavros/setpoint_position/local", PoseStamped, queue_size=10)
    local_pos_pub_2 = rospy.Publisher("/drone2/mavros/setpoint_position/local", PoseStamped, queue_size=10)

    collision_pub_1 = rospy.Publisher("/drone1/quad/quad_states", quad_states, queue_size=0)
    collision_pub_2 = rospy.Publisher("/drone2/quad/quad_states", quad_states, queue_size=0)


    rate = rospy.Rate(100) # 100 Hz

    while(not rospy.is_shutdown() and not current_state.connected):
        rate.sleep()

    pos_1 = PoseStamped()
    pos_2 = PoseStamped()
    collision = quad_states()

    while(not rospy.is_shutdown() ):
        des_coordinates_1[0] = coordinates_1[0]
        des_coordinates_1[1] = coordinates_1[1]
        des_coordinates_1[2] = coordinates_1[2]
        des_coordinates_1[3] = coordinates_1[3]
        des_coordinates_2[0] = coordinates_2[0]
        des_coordinates_2[1] = coordinates_2[1]
        des_coordinates_2[2] = coordinates_2[2]
        des_coordinates_2[3] = coordinates_2[3]

        check_collision()
        collision.collision=collision_1_2
        collision_pub_1.publish(collision)
        collision_pub_2.publish(collision)
        
        if(collision_1_2):
            avoid_collision()
            pos_1.pose.position.x = des_coordinates_1[0]
            pos_1.pose.position.y = des_coordinates_1[1]
            pos_1.pose.position.z = des_coordinates_1[2]
            pos_1.pose.orientation.x = des_coordinates_1[3]

            pos_2.pose.position.x = des_coordinates_2[0]
            pos_2.pose.position.y = des_coordinates_2[1]
            pos_2.pose.position.z = des_coordinates_2[2]
            pos_2.pose.orientation.x = des_coordinates_2[3]

            local_pos_pub_1.publish(pos_1)
            local_pos_pub_2.publish(pos_2)

        rate.sleep()
