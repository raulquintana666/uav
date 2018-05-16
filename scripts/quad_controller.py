#!/usr/bin/env python

import rospy
from std_msgs.msg import Int16

def motor1talker():
	pub = rospy.Publisher('motor1throttle', Int16, queue_size=10)     
	rospy.init_node('motor1talker', anonymous=True)
     	rate = rospy.Rate(10) # 10hz

     	while not rospy.is_shutdown():
         	throttle = 1500 % rospy.get_time()
         	rospy.loginfo(throttle)
         	pub.publish(throttle)
         	rate.sleep()
   
if __name__ == '__main__':
       	try:
           	motor1talker()
       	except rospy.ROSInterruptException:
           	pass	


