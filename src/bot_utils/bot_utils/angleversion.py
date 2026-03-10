#!/usr/bin/env python3
from urllib import request, response

import rclpy        
import rclpy
from rclpy.node import Node
from bot_msgs.srv import EulerToQu, QuToEuler
from tf_transformations import euler_from_quaternion, quaternion_from_euler

class angleversion(Node):
    def __init__(self):
        super().__init__('angle_conversion_service')
        self.service_ = self.create_service(EulerToQu, 'euler_to_quaternion', self.euler_to_quaternion_callback)
        self.service_ = self.create_service(QuToEuler, 'quaternion_to_euler', self.quaternion_to_euler_callback)
        self.get_logger().info("Service is ready to convert angles.")
    def euler_to_quaternion_callback(self, request, response):
        (response.x,response.y,response.z,response.w) =   quanternion = quaternion_from_euler(request.roll, request.pitch, request.yaw)
        (response.x,response.y,response.z,response.w) = quaternion_from_euler(request.roll, request.pitch, request.yaw)
        self.get_logger().info("Incoming request: roll=%f, pitch=%f, yaw=%f. Sending back response: x=%f, y=%f, z=%f, w=%f" % (request.roll, request.pitch, request.yaw, response.x, response.y, response.z, response.w))        
        return response
    def quaternion_to_euler_callback(self, request, response):
        (response.roll, response.pitch, response.yaw) = euler_from_quaternion([request.x, request.y, request.z, request.w]) 
        self.get_logger().info("Incoming request: x=%f, y=%f, z=%f, w=%f. Sending back response: roll=%f, pitch=%f, yaw=%f" % (request.x, request.y, request.z, request.w, response.roll, response.pitch, response.yaw))
        return response
def main():
    rclpy.init()
    angleversioner = angleversion()
    rclpy.spin(angleversioner)
    angleversioner.destroy_node()
    rclpy.shutdown()
    
if __name__ == "__main__":
    main()