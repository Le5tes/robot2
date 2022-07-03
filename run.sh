#!/bin/bash

echo "-- source ros --"
source /opt/ros/galactic/setup.bash

echo "-- source project --"
source ./install/setup.bash

echo "-- source web_video_server --"
source ../web_video_server/install/setup.bash

echo "-- launch! --"
ros2 launch robot websocket.launch.xml
