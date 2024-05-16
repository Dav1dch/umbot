cmake_minimum_required(VERSION 3.0.2)
project(tools)

# add_compile_options(-std=c++11)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  genmsg
  pcl_conversions
  pcl_ros
  message_generation
  livox_ros_driver2
)


catkin_package()

include_directories(include ${catkin_INCLUDE_DIRS} ${PCL_INCLUDE_DIRS}  /usr/include/eigen3)


add_executable(points_filter src/points_filter.cpp)
target_link_libraries(points_filter ${catkin_LIBRARIES} ${PCL_LIBRARIES})

