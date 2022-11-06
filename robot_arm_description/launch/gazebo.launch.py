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


    package_path = get_package_share_directory('robot_arm_description')
    robot_name = "robot_arm"
    xacro_file = package_path + '/description/xacro/' + robot_name + '.urdf.xacro'
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

    # Spawn the robot in Gazebo
    spawn_entity_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-entity', 'robot', '-topic', '/robot_description'],
        output='screen'
    )

    load_joint_state_broadcaster = ExecuteProcess(
        cmd=['ros2','control','load_controller','--set-state','active','joint_state_broadcaster'],
        output = 'screen',
    )

    load_trajectory_controller = ExecuteProcess(
        cmd=['ros2','control','load_controller','--set-state','active','joint_trajectory_controller'],
        output = 'screen',
    )



    # Start Gazebo with my empty world
    world_file_name = 'empty_world.world'
    world = os.path.join(package_path, 'worlds', world_file_name)
    gazebo_node = ExecuteProcess(
        cmd=['gazebo' ,'--verbose', world, '-s', 'libgazebo_ros_factory.so'], 
        output='screen',
    )

    return LaunchDescription([
        # RegisterEventHandler(
        #   event_handler=OnProcessExit(
        #         target_action=spawn_entity_robot,
        #         on_exit=[load_joint_state_broadcaster],
        #     )
        # ),
        # RegisterEventHandler(
        #     event_handler=OnProcessExit(
        #         target_action=load_joint_state_broadcaster,
        #         on_exit=[load_trajectory_controller],
        #     )
        # ),
        robot_state_publisher,
        spawn_entity_robot,
        gazebo_node, 
        # joint_state_publisher_gui,
        # load_joint_state_broadcaster,
        # load_trajectory_controller,
    ])
