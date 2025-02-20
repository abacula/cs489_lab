from irobot_create_msgs.msg import LightringLeds, AudioNote
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from sensor_msgs.msg import LaserScan

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data

class ScanTestNode(Node):
    def __init__(self):
        super().__init__('scan_test_node')

        # Cap velocity to 0.4 m/s
        self.vel_cap = 0.4

        self.obstacle = False


        # Subscirbe to scan
        self.scan_sub = self.create_subscription(LaserScan, '/robot1/scan', self.callback_scan, 10)
        self.scan_sub

        # Publisher for LEDs
        self.led_publish = self.create_publisher(LightringLeds, '/robot1/cmd_lightring', qos_profile_sensor_data)

     

 


    # Callback for scan
    def callback_scan(self, msg):
        range_min = msg.range_min
        range_max = msg.range_max

        self.obstacle = False

        self.get_logger().info(str(len(msg.ranges)))
        
        # front range is 200:340

        # meghan shows up in 234:302

        for angle in range(200,340):
            scan_point = msg.ranges[angle]
            
            if (scan_point <= range_min) or (scan_point >= range_max):
                pass
            else:
                self.get_logger().info(F"distance: {str(scan_point)}, angle: {str(angle)}")
                if scan_point <= 0.75:
                    # detect obstacle
                    #self.obstacle = True
                    self.get_logger().info("Obstacle detected!")

        # Publish LED to red if too fast, purple if obstacle
        light_msg = self.set_lightring_colors(self,self.obstacle)
        self.led_publish.publish(light_msg)


    # Set led colors based on velocity
    def set_lightring_colors(self,vel,obstacle):
        lightring_msg = LightringLeds()
        lightring_msg.header.stamp = self.get_clock().now().to_msg()
        lightring_msg.override_system = True
        if obstacle:
            for i in range(6):
                lightring_msg.leds[i].red = 255
                lightring_msg.leds[i].blue = 255
                lightring_msg.leds[i].green = 0


        return lightring_msg

   
        
        

def main(args=None):
    rclpy.init(args=args)
    node = ScanTestNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()