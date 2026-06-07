source /opt/ros/lyrical/setup.bash

colcon build --packages-select robot
source ./install/setup.bash

ros2 launch robot websocket.launch.xml