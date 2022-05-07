### Install script
# Sets up ROS2 Galactic, installs dependencies and builds the package
# --Run with sudo--

# ensure locale set up properly
apt update && apt install locales
locale-gen en_GB en_GB.UTF-8
update-locale LC_ALL=en_GB.UTF-8 LANG=en_GB.UTF-8
export LANG=en_GB.UTF-8

# ensure universe repository available
apt install software-properties-common
add-apt-repository universe

# add ros repositories
apt update && apt install curl gnupg lsb-release
curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(lsb_release -c --short) main" | tee /etc/apt/sources.list.d/ros2.list > /dev/null
apt update

# install ros
apt install ros-galactic-ros-base

# Source ROS
. /opt/ros/galactic/setup.bash

# Add dependencies!
apt install python3-rosdep
rosdep init
rosdep update
rosdep install --from-paths src --ignore-src -r -y --rosdistro galactic

# Build package
apt install python3-colcon-common-extensions
colcon build --packages-select robot
. ./install/setup.bash