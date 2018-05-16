#!/usr/bin/env python

import rospy
from std_msgs.msg import Int16

def motor4talker():
	pub = rospy.Publisher('motor4throttle', Int16, queue_size=10)     
	rospy.init_node('motor4talker', anonymous=True)
     	rate = rospy.Rate(10) # 10hz

     	while not rospy.is_shutdown():
         	throttle4 = 1600 % rospy.get_time()
         	rospy.loginfo(throttle4)
         	pub.publish(throttle4)
         	rate.sleep()
   
if __name__ == '__main__':
       	try:
           	motor4talker()
       	except rospy.ROSInterruptException:
           	pass
