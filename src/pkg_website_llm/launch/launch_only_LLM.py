from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
import os

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='pkg_website_llm',
            namespace='LLM',
            executable='pack_item_server',
            output='screen',
            name='pack_item_server'
        ),
    ])