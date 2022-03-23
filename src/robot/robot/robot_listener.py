import rclpy
from rclpy.node import Node
from robot.robot_controller import RobotController
from std_msgs.msg import String

class RobotControlListener(Node):
  def __init__(self):
    super().__init__('robot_controller')
    self.robot = RobotController()
    self.sub = self.create_subscription(String,'/usr_cmd',self.give_command,10)

  def give_command(self, command):
    self.robot.give_command(command.data)

def main(args=None):
  rclpy.init(args=args)
  node = RobotControlListener()
  rclpy.spin(node)
  node.destroy_node()
  rclpy.shutdown()
  
if __name__ == "__main__":
  main()