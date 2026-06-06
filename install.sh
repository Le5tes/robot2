#!/bin/bash

### Install script
# Sets up ROS2 Lyrical, installs dependencies and builds the package
# --Run with sudo--
# -- Run from within this folder --

echo "-- stupid apt unattended upgrades - we need to access that lock file! --"
systemctl stop unattended-upgrades
apt remove unattended-upgrades

echo "-- ensure locale set up properly --"
apt update && apt install locales
locale-gen en_GB en_GB.UTF-8
update-locale LC_ALL=en_GB.UTF-8 LANG=en_GB.UTF-8
export LANG=en_GB.UTF-8

echo "-- ensure universe repository available --"
apt install software-properties-common
add-apt-repository universe

echo "-- add ros repositories --"
apt update && apt install curl gnupg lsb-release
curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(lsb_release -c --short) main" | tee /etc/apt/sources.list.d/ros2.list > /dev/null
apt update

echo "-- install ros --"
apt install ros-lyrical-ros-base

echo "-- source ros --"
source /opt/ros/lyrical/setup.bash

echo "-- add dependencies --"
apt install python3-rosdep
rosdep init
rosdep update
rosdep install --from-paths src --ignore-src -r -y --rosdistro lyrical
apt install python3-colcon-common-extensions

echo "get webserver"
apt install g++
apt install ros-lyrical-web-video-server

echo "-- add gpiozero --"
apt install python3-gpiozero python3-pigpio

echo "-- add vision dependencies --"
apt install python3-picamera2 python3-opencv

echo "-- build packages --"

colcon build --packages-select robot
source ./install/setup.bash

echo "-- set to run on startup --"
LAUNCH_FILE=/etc/rc.local
WORKING_DIR=$(pwd)
if [ ! -f "$LAUNCH_FILE" ]; then
  echo '#!/bin/bash' >> $LAUNCH_FILE
  chmod 755 $LAUNCH_FILE
fi
echo "${WORKING_DIR}/run.sh" >> $LAUNCH_FILE

echo "-- launch! --"
ros2 launch robot websocket.launch.xml