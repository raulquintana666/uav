#!/usr/bin/env python
from __future__ import division
import rospy
from std_msgs.msg import Float32
from std_msgs.msg import Int16
from sensor_msgs.msg import Joy
from datetime import datetime

KP = 0.1
KI = 0.0
KD = 0.002

#user input variables
user_throttle = 0.0
user_roll = 0.0
user_pitch = 0.0
user_yaw = 0.0
user_a_button = 0

#timestep variable
dt = 1

# roll variables
current_roll = 0.0
roll_adjust = 0.0
roll_proportional = 0.0
roll_integral = 0.0
roll_derivative = 0.0
roll_error_previous = 0.0

# pitch variables
current_pitch = 0.0
pitch_adjust = 0.0
pitch_proportional = 0.0
pitch_integral = 0.0
pitch_derivative = 0.0
pitch_error_previous = 0.0

# yaw variables
current_yaw = 0.0
yaw_adjust = 0.0
yaw_proportional = 0.0
yaw_integral = 0.0
yaw_derivative = 0.0
yaw_error_previous = 0.0

# subscribers TO CONTROLLER SPLITTER DATA
def throttle_read(data):
	global user_throttle
	user_throttle = data.data * 1000 +1000

def roll_read(data):
	global user_roll
	user_roll = data.data * (-500)
	
def pitch_read(data):
	global user_pitch
	user_pitch = data.data * (500)

def yaw_read(data):
	global user_yaw
	user_yaw = data.data * (500)

def a_button_read(data):
	global user_a_button
	user_a_button = data.data

# subscribers to gyro data
def gyro_x_read(data):
	global current_roll
	current_roll = data.data 
    
def gyro_y_read(data):
	global current_pitch
	current_pitch = data.data 
	    
# Intializes everything
def start():
	
	
	
	global user_throttle
	global user_roll
	global user_pitch
	global user_yaw
	global user_a_button
	
	global dt
	
	global roll_adjust
	global roll_proportional
	global roll_integral
	global roll_derivative
	global roll_error_previous
	
	global pitch_adjust
	global pitch_proportional
	global pitch_integral
	global pitch_derivative
	global pitch_error_previous
	
	global yaw_adjust
	global yaw_proportional
	global yaw_integral
	global yaw_derivative
	global yaw_error_previous
	
    ################## PUBLISHERS #################################################
    # initializing the publisher for thumb value, redundant
	#left_thumb_pub = rospy.Publisher('left_stick_reading', Float32, queue_size=10)
	motor1pub = rospy.Publisher('motor1throttle', Float32, queue_size=1)
	motor2pub = rospy.Publisher('motor2throttle', Float32, queue_size=1)
	motor3pub = rospy.Publisher('motor3throttle', Float32, queue_size=1)
	motor4pub = rospy.Publisher('motor4throttle', Float32, queue_size=1)
	
    ##################### START THIS NODE ####################################
    #naming this node
	rospy.init_node('motor_commands')
    
    ################## SUBSCRIBERS #################################################
    # subscribing to the controller splitter topics
	rospy.Subscriber("user_throttle", Float32, throttle_read)
	rospy.Subscriber("user_pitch", Float32, pitch_read)
	rospy.Subscriber("user_roll", Float32, roll_read)
	rospy.Subscriber("user_yaw", Float32, yaw_read)
	rospy.Subscriber("user_a_button", Int16, a_button_read)
	
    # subscribing to the gyro_x_cal_node node
	rospy.Subscriber("gyro_x_cal", Float32, gyro_x_read)
    
    # subscribing to the gyro_y_cal_node node
	rospy.Subscriber("gyro_y_cal", Float32, gyro_y_read)
    
	r = rospy.Rate(100)
	
	####################### MAIN LOOP ##################################
	while not rospy.is_shutdown():
		
		start = datetime.now()
		
		####################### ROLL CONTROL ##########################
		roll_error = user_roll - current_roll
		
		roll_proportional = KP * roll_error
		roll_integral += KI * roll_error * dt/1000000
		roll_derivative = KD * (roll_error - roll_error_previous)/dt
		
		roll_error_previous = roll_error
		
		roll_adjust = roll_proportional + roll_integral + roll_derivative
		
		####################### PITCH CONTROL ##########################
		pitch_error = user_pitch - current_pitch
		
		pitch_proportional = KP * pitch_error
		pitch_integral += KI * pitch_error * dt/1000000
		pitch_derivative = KD * (pitch_error - pitch_error_previous)/dt
		
		pitch_error_previous = roll_error
		
		pitch_adjust = pitch_proportional + pitch_integral + pitch_derivative
		
		####################### YAW CONTROL ##########################
		yaw_error = user_yaw - current_yaw
		
		yaw_proportional = KP * yaw_error
		yaw_integral += KI * yaw_error * dt/1000000
		yaw_derivative = KD * (yaw_error - yaw_error_previous)/dt
		
		yaw_error_previous = yaw_error
		
		yaw_adjust = yaw_proportional + yaw_integral + yaw_derivative
		
		####################### TIME CALC ###############################
		end = datetime.now()
		dt = end.microsecond - start.microsecond

		##################### MOTOR COMMANDS #################
		motor1 = user_throttle - pitch_adjust + roll_adjust - yaw_adjust
		motor2 = user_throttle - pitch_adjust - roll_adjust + yaw_adjust 
		motor3 = user_throttle + pitch_adjust + roll_adjust + yaw_adjust
		motor4 = user_throttle + pitch_adjust - roll_adjust - yaw_adjust
		
		############## MOTOR PUBLISHING #############################
		
		if motor1 > 2000 and user_a_button != 1:
			motor1 = 2000
		elif motor1 < 1000 and user_a_button != 1:
			motor1 = 1000
		elif user_a_button == 1:
			motor1 = 1000
		motor1pub.publish(motor1)
				
		if motor2 > 2000 and user_a_button != 1:
			motor2 = 2000
		elif motor2 < 1000 and user_a_button != 1:
			motor2 = 1000
		elif user_a_button == 1:
			motor2 = 0
		motor2pub.publish(motor2)
        
		if motor3 > 2000 and user_a_button != 1:
			motor3 = 2000
		elif motor3 < 1000 and user_a_button != 1:
			motor3 = 1000
		elif user_a_button == 1:
			motor3 = 1000
		motor3pub.publish(motor3)
		
		if motor4 > 2000 and user_a_button != 1:
			motor4 = 2000
		elif motor4 < 1000 and user_a_button != 1:
			motor4 = 1000
		elif user_a_button == 1:
			motor4 = 1000
		motor4pub.publish(motor4)

		r.sleep()
	

if __name__ == '__main__':
    start()
