#!/bin/bash

## Important to start the on-off controller first!
# This controls the power supply to the pi - when the on button is pressed we get ~20s 
# to boot up and start outputting a signal that will keep the pi powered up.
python3 ./on-off-controller.py -i 24 -o 25 &

echo "-- source ros --"
source /opt/ros/kilted/setup.bash

echo "-- source project --"
source ./install/setup.bash

echo "-- source web_video_server --"
source ../web_video_server/install/setup.bash

echo "-- launch! --"
ros2 launch robot websocket.launch.xml
