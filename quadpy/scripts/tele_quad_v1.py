#!/usr/bin/env python
import rospy
from random import random

from std_msgs.msg import Float32
from sensor_msgs.msg import Joy

throttle_reading = 0.0

def controller_read(data):
	
	global throttle_reading
    ### thumbstick values ###
    # the left thumb value velocity is the up or down value read from the controller (-1,1)
	throttle_reading = data.axes[1] 

    
# Intializes everything
def start():
	
	
	#declaring publisher for left thumb value
	global left_thumb_pub
	global throttle_reading
    
    # initializing the publisher for thumb value, redundant
	left_thumb_pub = rospy.Publisher('left_stick_reading', Float32, queue_size=10)
    
    #starting the node
	rospy.init_node('motor_commands')
    
    # subscribing to the joy node
	joy_sub = rospy.Subscriber("joy", Joy, controller_read)
    
	r = rospy.Rate(100)
	while not rospy.is_shutdown():
	
		global throttle_reading
		
        #publishng the control value, for testing
		left_thumb_pub.publish(throttle_reading)
        
		r.sleep()

if __name__ == '__main__':
    start()
