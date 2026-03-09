from launch import LaunchDescription
from pathlib import Path
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument , SetEnvironmentVariable, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
import os 
from ament_index_python.packages import get_package_share_directory 
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command , LaunchConfiguration

bot_desc_dir =get_package_share_directory('bot_desc')
def generate_launch_description():
    model_arg = DeclareLaunchArgument(
        name="model",
        default_value=os.path.join(bot_desc_dir,"urdf","model.urdf.xacro"),
        description="path to the urdf file"
                                      
                                      )
    
    Gazebo_resource_path = SetEnvironmentVariable(name="GZ_SIM_RESOURCE_PATH",
                                value=str(Path(bot_desc_dir).parent.resolve()))
    ros_distro = os.environ["ROS_DISTRO"]
    is_ignition = "True" if ros_distro == "humble" else "False"
    R_desc =  ParameterValue(Command(["xacro ", 
                                      LaunchConfiguration("model"),
                                      " is_ignition:=",is_ignition
                                      ]),
                             value_type=str)
    
    
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": R_desc, 
                     "use_sim_time": True}]
      )
    gazebo= IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(get_package_share_directory('ros_gz_sim'),
                                                    'launch'),"/gz_sim.launch.py"] ),
        launch_arguments=[("gz_args", ["-v 4 -r empty.sdf"])]
        )
    
    gazebo_spawn_entity = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=["-topic", "robot_description", 
                   "-name", "prototype"],
        output="screen" )

    gz_ros2_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=["/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock",
            "/image_raw@sensor_msgs/msg/Image[gz.msgs.Image",
            "/camera_info@sensor_msgs/msg/CameraInfo[gz.msgs.CameraInfo",])
    
    
    
    return LaunchDescription([
        model_arg,
        Gazebo_resource_path,
        robot_state_publisher,
        gazebo,
        gazebo_spawn_entity,
        gz_ros2_bridge,
        
        
    ])