#!/usr/bin/env python
from __future__ import division
import rospy
from std_msgs.msg import Float32
from std_msgs.msg import Int16
from sensor_msgs.msg import Joy
from datetime import datetime

# this program takes in user input from xbox 360 controller and publishes them as 
# 	the appropriate axes 
throttle = 0.0
roll = 0.0
pitch = 0.0
yaw = 0.0
a_button = 0

############## SUBSCRIBER CALLBACK ##############################################
def controller_read(data):

	global throttle
	global roll
	global pitch
	global yaw
	global a_button
    ### thumbstick values ###
    # the left thumb value velocity is the up or down value read from the controller (-1,1)
	roll = data.axes[3]
	pitch = data.axes[4]
	yaw = data.axes[0]
	throttle = data.axes[1]
	a_button = data.buttons[0]


def start():
	
	global throttle
	global roll
	global pitch
	global a_button
	
    ################## PUBLISHERS #################################################
    # initializing the publisher for thumb value, redundant
	#left_thumb_pub = rospy.Publisher('left_stick_reading', Float32, queue_size=10)
	throttlepub = rospy.Publisher('user_throttle', Float32, queue_size=1)
	rollpub = rospy.Publisher('user_roll', Float32, queue_size=1)
	pitchpub = rospy.Publisher('user_pitch', Float32, queue_size=1)
	yawpub = rospy.Publisher('user_yaw', Float32, queue_size=1)
	a_buttonpub = rospy.Publisher('user_a_button', Int16, queue_size=1)
	
    ##################### START THIS NODE ####################################
    #starting the node
	rospy.init_node('user_flight_commands')
    
    ################## SUBSCRIBERS #################################################
    # subscribing to the joy node
	rospy.Subscriber("joy", Joy, controller_read)
	
    
	r = rospy.Rate(200)
	
	# MAIN LOOP 
	while not rospy.is_shutdown():

		
		############## USER FLIGHT DATA PUBLISHING #############################
		
		throttlepub.publish(throttle)
		pitchpub.publish(pitch)
		rollpub.publish(roll)
		yawpub.publish(yaw)
		a_buttonpub.publish(a_button)

		r.sleep()
	

if __name__ == '__main__':
    start()
