import gpiozero
import rclpy
from rclpy.node import Node
from rclpy.subscription import Subscription

class RobotController:
  def __init__(self):
    self.robot = gpiozero.Robot(left=(17,18), right=(22,27))

  def give_command(self, command):
    print(command)
    if command == "forward":
      self.robot.forward()
    elif command == "back":
      self.robot.backward()
    elif command == "right":
      self.robot.right()
    elif command == "left":
      self.robot.left()
    elif command == "stop":
      self.robot.stop()
    else:
      return "Command not recognised"
    return command

class RobotControlListener(Node):
  def __init__(self):
    super.__init__('robot_controller')
    self.robot = RobotController()
    self.sub = self.create_subscription('std_msgs/String','/usr_cmd',self.give_command,10)

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