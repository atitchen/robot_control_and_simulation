import os

from click import launch
from launch_ros.actions import Node
from launch import LaunchDescription
from launch.substitutions import Command
from launch.actions import ExecuteProcess, IncludeLaunchDescription, RegisterEventHandler
from launch.event_handlers import (OnProcessStart, OnProcessExit)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory

# from moveit_configs_utils import MoveItConfigsBuilder


def generate_launch_description():


    package_path = get_package_share_directory('mrm_sim')
    robot_name = "mrm_001"
    xacro_file = package_path + '/description/xacro/' + "mrm_001" + '.urdf.xacro'
    robot_desc = Command(['xacro', ' ', xacro_file])

    # Robot State Publisher 
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='both',
        parameters=[{'robot_description': robot_desc}]
     )

    # Joint State Publisher 
    joint_state_publisher_gui = Node(
		package  ='joint_state_publisher_gui',
		executable='joint_state_publisher_gui',
		output    ='screen',
		name      ='joint_state_publisher_gui',
	)


    # RViz
    rviz_config_file = package_path + '/rviz/view_config.rviz'
    rviz_node = Node(package    ='rviz2',
					 executable ='rviz2',
					 name       ='rviz2',
					 output     ='log',
					 arguments  =['-d', rviz_config_file])

    

    return LaunchDescription([
        robot_state_publisher,
        rviz_node, 
        joint_state_publisher_gui,
    ])
