#!/bin/bash

### Install script
# Sets up ROS2 Galactic, installs dependencies and builds the package
# --Run with sudo--

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
apt install ros-galactic-ros-base

echo "-- source ros --"
source /opt/ros/galactic/setup.bash

echo "-- add dependencies --"
apt install python3-rosdep
rosdep init
rosdep update
rosdep install --from-paths src --ignore-src -r -y --rosdistro galactic
apt install python3-colcon-common-extensions

echo "get webserver"
apt install g++
cd ..
git clone git@github.com:Le5tes/web_video_server.git
cd web_video_server
git checkout built-ros2
git pull

rosdep install --from-paths ./ --ignore-src -r -y --rosdistro galactic

source ./install/setup.bash
cd ../robot2

echo "-- add gpiozero --"
apt install python3-gpiozero python3-pigpio

echo "-- build package --"

colcon build --packages-select robot
source ./install/setup.bash

echo "-- set to run on startup --"
LAUNCH_FILE=/etc/rc.local
WORKING_DIR=$(pwd)
if [ ! -f "$LAUNCH_FILE" ]; then
  echo '#!/bin/bash' >> $LAUNCH_FILE
fi
echo "${WORKING_DIR}/run.sh" >> $LAUNCH_FILE

echo "-- launch! --"
ros2 launch robot websocket.launch.xml