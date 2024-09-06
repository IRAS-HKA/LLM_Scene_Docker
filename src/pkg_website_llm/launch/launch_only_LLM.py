from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
import os

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='pkg_llm_docker',
            namespace='LLM',
            executable='llm_action_server',
            output='screen',
            name='LLM1'
        ),
        Node(
            package='pkg_website_llm',
            namespace='LLM',
            executable='action_server_client',
            output='screen',
            name='LLM_ActionClient'
        ),
    ])