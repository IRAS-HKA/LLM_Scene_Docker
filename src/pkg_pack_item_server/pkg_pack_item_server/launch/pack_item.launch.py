import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration



def generate_launch_description():
    os.environ['PYTHONPATH'] = '/home/robot/ros_ws/src/pkg_pack_item_server/pkg_pack_item_server' + os.environ.get('PYTHONPATH', '')

    return LaunchDescription([
        Node(
            package='pkg_pack_item_server',
            executable='pack_item_server',
            output='screen',
        ),
    ])
