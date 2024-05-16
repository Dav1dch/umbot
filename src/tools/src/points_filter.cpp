#include "livox_ros_driver2/CustomMsg.h"
#include "livox_ros_driver2/CustomPoint.h"
#include <pcl/point_cloud.h>
#include <pcl/point_types.h>
#include <pcl_conversions/pcl_conversions.h>
#include <ros/ros.h>
#include <sensor_msgs/PointCloud2.h>
#include <std_msgs/String.h>

ros::Publisher filtered_points_pub;

void callback(const sensor_msgs::PointCloud2ConstPtr &input) {
  livox_ros_driver2::CustomMsg livox_filtered_ponits;
  livox_filtered_ponits.header = input->header;
  // livox_filtered_ponits->header.stamp = input->header.stamp;
  // livox_filtered_ponits->header.seq = input->header.seq;
  // livox_filtered_ponits->header.frame_id = input->header.frame_id;
  // ROS_INFO("after");
  pcl::PointCloud<pcl::PointXYZI> points;
  pcl::PointCloud<pcl::PointXYZI> filtered_points;
  pcl::fromROSMsg(*input, points);
  filtered_points.header = points.header;

  uint count = 0;
  for (pcl::PointCloud<pcl::PointXYZI>::const_iterator iter = points.begin();
       iter != points.end(); iter++) {
    const pcl::PointXYZI &p = *iter;
    livox_ros_driver2::CustomPoint livoxp;
    if (!(p.x < 0 && p.x > -0.4)) {
      livoxp.x = p.x;
      livoxp.y = p.y;
      livoxp.z = p.z;
      livoxp.reflectivity = p.intensity;
      count++;
      filtered_points.points.push_back(p);
      livox_filtered_ponits.points.push_back(livoxp);
    }
    livox_filtered_ponits.point_num = count;
  }

  pcl::PointCloud<pcl::PointXYZI>::Ptr filtered(
      new pcl::PointCloud<pcl::PointXYZI>(filtered_points));
  sensor_msgs::PointCloud2 filtered_msg;
  pcl::toROSMsg(*filtered, filtered_msg);

  filtered_points_pub.publish(livox_filtered_ponits);
}

int main(int argc, char **argv) {
  ros::init(argc, argv, "points_filter");
  ROS_INFO("hello world");
  ros::NodeHandle nh;

  ros::Subscriber sub = nh.subscribe("/livox/lidar", 10, callback);
  filtered_points_pub =
      nh.advertise<livox_ros_driver2::CustomMsg>("/livox/filtered_lidar", 10);
  ros::spin();
  return 0;
}
