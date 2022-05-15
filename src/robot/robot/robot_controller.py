import gpiozero
import os

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
    elif command == "shutdown":
      os.system("shutdown -h now")
    else:
      return "Command not recognised"
    return command
