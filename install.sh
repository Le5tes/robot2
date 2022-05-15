#!/bin/bash

### Install script
# Sets up ROS2 Galactic, installs dependencies and builds the package
# --Run with sudo--

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
apt install ros-galactic-ros-base

echo "-- source ros --"
source /opt/ros/galactic/setup.bash

echo "-- add dependencies --"
apt install python3-rosdep
rosdep init
rosdep update
rosdep install --from-paths src --ignore-src -r -y --rosdistro galactic

echo "-- add gpiozero --"
apt install python3-gpiozero python3-pigpio

echo "Build package"
apt install python3-colcon-common-extensions
colcon build --packages-select robot
source ./install/setup.bash

echo "-- launch! --"
ros2 launch robot websocket.launch.xml