from launch import LaunchDescription
from pathlib import Path
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument , SetEnvironmentVariable, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
import os 
from ament_index_python.packages import get_package_share_directory 
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command , LaunchConfiguration

def generate_launch_description():
    robot_description = ParameterValue(
        Command(
            [
                "xacro ",
                os.path.join(get_package_share_directory("bot_desc"),"urdf","model.urdf.xacro")
            ]
        ),
        value_type=str,
        
    )
    
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robot_description}]
      )
    controller_manager = Node(
        
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[
            {"robot_description": robot_description},
            os.path.join(get_package_share_directory("bot_controller"),"config","bot_controllers.yaml")
        ]
    )    
    
    joint_state_spawner= Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "joint_state_broadcaster",
            "--controller-manager",
            "/controller_manager"
        ]
    )
    
    arm_controller_spawner= Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "arm_controller",
            "--controller-manager",
            "/controller_manager"
        ]
    )
    
    gripper_controller_spawner= Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "gripper_controller",
            "--controller-manager",
            "/controller_manager"
        ]
    )
            
    
    
    return LaunchDescription([
        robot_state_publisher,
        controller_manager,
        joint_state_spawner,
        arm_controller_spawner,
        gripper_controller_spawner
        ])