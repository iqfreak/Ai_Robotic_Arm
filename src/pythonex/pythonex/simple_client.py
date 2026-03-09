import rclpy
from rclpy.node import Node
from bot_msgs.srv import AddTwo
import sys
class simpleclient(Node):
    def __init__(self,a,b):
        super().__init__('simple_client')
        self.client_ = self.create_client(AddTwo, 'add_two_ints')
        while not self.client_.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')
        self.req = AddTwo.Request()
        self.req.a = a
        self.req.b = b
        self.future = self.client_.call_async(self.req)
        self.future.add_done_callback(self.response_callback)
    def response_callback(self, future):
        try:
            response = future.result()
            self.get_logger().info("Result of add_two_ints: %d + %d = %d" % (self.req.a, self.req.b, response.sum))
        except Exception as e:
            self.get_logger().error("Service call failed: %r" % (e,))
            
            
            
            
def main():        
    rclpy.init()
    if len(sys.argv) != 3:
        print("Usage: simple_client.py <int a> <int b>")
        return -1 
    simple_client = simpleclient(int(sys.argv[1]), int(sys.argv[2]))
    rclpy.spin(simple_client)
    simple_client.destroy_node()
    rclpy.shutdown()
if __name__ == "__main__":        
    main()