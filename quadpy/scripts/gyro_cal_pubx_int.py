#!/usr/bin/env python
from __future__ import division
import rospy
from datetime import datetime 
from std_msgs.msg import Float32
from std_msgs.msg import Int16
import time

# CONSTANTS
GYRO_PART = 0.995
ACC_PART = 0.005
GYRO_ANGLE_SCALE_FACTOR = 90/650 # this works
ACCEL_SCALE_FACTOR = 90/270 # this works
LOOPRATE = 100
TIMESTEP = 1/LOOPRATE

# VARIABLES
gyro_in = 0
accel_in = 0
gyro_last_update = datetime.now()
gyro_angle = 0.0
delta_t = 0.0


#function gyro_callback
#purpose:
# 1. read gyro input
# 2. save it to a variable
def gyro_callback(data):
    global gyro_in
    gyro_in = data.data

#function accel_callback
#purpose:
# 1. read gyro input
# 2. save it to a variable
def accel_callback(data):
    global accel_in
    accel_in = data.data

# function: calc_offset
# purpose: calculates gyro offset and returns it
def calc_gyro_offset():

	x = 0.0
	
	for i in range(10):
		# get gyro val 
		#gyro_in = random.uniform(9,11)
		
		x = x + gyro_in
		
		#wait 0.1s
		time.sleep(0.1)
	
	# divide by 10 to get average
	x = x/10
	return x

def calc_accel_offset():

	x = 0.0
	
	for i in range(10):
		# get gyro val 
		#gyro_in = random.uniform(9,11)
		
		x = x + accel_in
		
		#wait 0.1s
		time.sleep(0.1)
	
	# divide by 10 to get average
	x = x/10
	return x

# function: gyro_cal_pub    
def start():
	
	global gyro_in
	global gyro_rate
	global offset
	global gyro_angle
	global delta_t
	global gyro_last_update
	
	########### START PUBLISHERS ########################
	# starting the publishing node for rates
	gyro_out = rospy.Publisher('gyro_x_cal', Float32, queue_size=1)
	
	# starting the publishing node for angles
	gyro_out_angle = rospy.Publisher('gyro_x_angle', Float32, queue_size=1)
	
	# starting the publishing node for combined angles
	angle_combined = rospy.Publisher('angle_x_comb', Float32, queue_size=1)
	
	########### START NODES #############################
	
	# starting THIS nodes name
	rospy.init_node('gyro_x_cal_node', anonymous=True)
	
	# subscribing to the spec. gyro node named "gyro_x"
	rospy.Subscriber("gyro_x", Float32, gyro_callback)
	
	# subscribing to the spec. accel node named "accel_x"
	rospy.Subscriber("accel_x", Float32, accel_callback)
    
    # use the function to calibrate gyro 
	gyro_offset = calc_gyro_offset()
	accel_offset = calc_accel_offset()
	
    
	# MUST DO THIS FOR SUBSCRIBER PUBLISHER PROGRAMS TO UPDATE MORE THAN ONCE 
    # DO NOT USE SPIN
    # setting the publishing rate rospy.Rate(Hz)
	r = rospy.Rate(LOOPRATE)
    
	while not rospy.is_shutdown():
    		
    	# subtract the gyro offset (missing here)
		gyro_rate = (gyro_in - gyro_offset)
		accel_angle = (accel_in - accel_offset) * ACCEL_SCALE_FACTOR
		
    	# get the current time
		nowtime = datetime.now()
		
    	# calculate timestep and convert to seconds
		delta_t = ( nowtime.microsecond - gyro_last_update.microsecond ) / 1000000
		
		# perform the integration by having a running sum of rate * timestep
		#if delta_t < 0:
		#	delta_t = 1/LOOPRATE
		
		gyro_angle += gyro_rate * delta_t			
		
		# scale gyro
		gyro_angle = gyro_angle 
		
		combined_angle = GYRO_PART * (gyro_angle * GYRO_ANGLE_SCALE_FACTOR + (gyro_rate * delta_t)) + ACC_PART * accel_angle

		# save the time last time
		gyro_last_update = datetime.now()
		
		########## PUBLISHERS #######################
		
		#publish corrected gyro data
		gyro_out.publish(gyro_rate)
		
		#publish calculated angle from corrected gyro data
		gyro_out_angle.publish(gyro_angle * GYRO_ANGLE_SCALE_FACTOR)
		
		#publish calculated angle from combined accel and gyro angle data
		angle_combined.publish(combined_angle)
		
		r.sleep()


   
if __name__ == '__main__':
    start()


