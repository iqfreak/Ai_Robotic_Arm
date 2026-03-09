import rclpy
from rclpy.node import Node
from bot_msgs.srv import AddTwo

class simpleservice(Node):
    def __init__(self):
        super().__init__('simple_service')
        self.service_ = self.create_service(AddTwo, 'add_two_ints', self.service_callback)
        self.get_logger().info("Service is ready to add two ints.")
    def service_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info("Incoming request: a=%d, b=%d. Sending back response: sum=%d" % (request.a, request.b, response.sum))
        return response
    

def main():
    rclpy.init()
    simple_service = simpleservice()
    rclpy.spin(simple_service)
    simple_service.destroy_node()
    rclpy.shutdown()
    
if __name__ == "__main__":
    main()