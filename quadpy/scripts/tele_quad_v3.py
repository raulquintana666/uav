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

throttle_in = 0.0
a_button_state = 1
dt = 1

desired_roll = 0.0
current_roll = 0.0
roll_adjust = 0.0
roll_proportional = 0.0
roll_integral = 0.0
roll_derivative = 0.0
roll_error_previous = 0.0

desired_pitch = 0.0
current_pitch = 0.0
pitch_adjust = 0.0
pitch_proportional = 0.0
pitch_integral = 0.0
pitch_derivative = 0.0
pitch_error_previous = 0.0

# subscriber to joystick stuff
def controller_read(data):
	global throttle_in
	global desired_roll
	global desired_pitch
	global a_button_state
    ### thumbstick values ###
    # the left thumb value velocity is the up or down value read from the controller (-1,1)
	desired_roll = data.axes[3]*(-500)
	desired_pitch = data.axes[4]*(500)
	
	throttle_in = data.axes[1]*(1000) + 1000
	a_button_state = data.buttons[0]

def gyro_x_read(data):
	global current_roll
    ### thumbstick values ###
    # the left thumb value velocity is the up or down value read from the controller (-1,1)
	current_roll = data.data 
    
def gyro_y_read(data):
	global current_pitch
    ### thumbstick values ###
    # the left thumb value velocity is the up or down value read from the controller (-1,1)
	current_pitch = data.data 
	    
# Intializes everything
def start():
	
	
	
	global throttle_in
	global desired_roll
	global desired_pitch
	global a_button_state
	
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
	
    ################## PUBLISHERS #################################################
    # initializing the publisher for thumb value, redundant
	#left_thumb_pub = rospy.Publisher('left_stick_reading', Float32, queue_size=10)
	motor1pub = rospy.Publisher('motor1throttle', Float32, queue_size=1)
	motor2pub = rospy.Publisher('motor2throttle', Float32, queue_size=1)
	motor3pub = rospy.Publisher('motor3throttle', Float32, queue_size=1)
	motor4pub = rospy.Publisher('motor4throttle', Float32, queue_size=1)
    ##################### START THIS NODE ####################################
    #starting the node
	rospy.init_node('motor_commands')
    
    ################## SUBSCRIBERS #################################################
    # subscribing to the joy node
	rospy.Subscriber("joy", Joy, controller_read)
	
    # subscribing to the gyro_x_cal_node node
	rospy.Subscriber("gyro_x_cal", Float32, gyro_x_read)
    
    # subscribing to the gyro_y_cal_node node
	rospy.Subscriber("gyro_y_cal", Float32, gyro_y_read)
    
	r = rospy.Rate(100)
	
	####################### MAIN LOOP ##################################
	while not rospy.is_shutdown():
		
		start = datetime.now()
		
		####################### ROLL CONTROL ##########################
		roll_error = desired_roll - current_roll
		
		roll_proportional = KP * roll_error
		roll_integral += KI * roll_error * dt/1000000
		roll_derivative = KD * (roll_error - roll_error_previous)/dt
		
		roll_error_previous = roll_error
		
		roll_adjust = roll_proportional + roll_integral + roll_derivative
		
		####################### PITCH CONTROL ##########################
		pitch_error = desired_pitch - current_pitch
		
		pitch_proportional = KP * pitch_error
		pitch_integral += KI * pitch_error * dt/1000000
		pitch_derivative = KD * (pitch_error - pitch_error_previous)/dt
		
		pitch_error_previous = roll_error
		
		pitch_adjust = pitch_proportional + pitch_integral + pitch_derivative
		
		####################### TIME CALC ###############################
		end = datetime.now()
		dt = end.microsecond - start.microsecond

		##################### MOTOR COMMANDS #################
		motor1 = throttle_in - pitch_adjust + roll_adjust
		motor2 = throttle_in - pitch_adjust - roll_adjust 
		motor3 = throttle_in + pitch_adjust + roll_adjust
		motor4 = throttle_in + pitch_adjust - roll_adjust
		
		############## MOTOR PUBLISHING #############################
		
		if motor1 > 2000 and a_button_state != 1:
			motor1 = 2000
		elif motor1 < 1000 and a_button_state != 1:
			motor1 = 1000
		elif a_button_state == 1:
			motor1 = 1000
		motor1pub.publish(motor1)
				
		if motor2 > 2000 and a_button_state != 1:
			motor2 = 2000
		elif motor2 < 1000 and a_button_state != 1:
			motor2 = 1000
		elif a_button_state == 1:
			motor2 = 0
		motor2pub.publish(motor2)
        
		if motor3 > 2000 and a_button_state != 1:
			motor3 = 2000
		elif motor3 < 1000 and a_button_state != 1:
			motor3 = 1000
		elif a_button_state == 1:
			motor3 = 1000
		motor3pub.publish(motor3)
		
		if motor4 > 2000 and a_button_state != 1:
			motor4 = 2000
		elif motor4 < 1000 and a_button_state != 1:
			motor4 = 1000
		elif a_button_state == 1:
			motor4 = 1000
		motor4pub.publish(motor4)

		r.sleep()
	

if __name__ == '__main__':
    start()
