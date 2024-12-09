from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
import os

def generate_launch_description():
    return LaunchDescription([     
        Node(
            package='pkg_website_llm',
            namespace='LLM',
            executable='website_llm',
            output='screen',
            name='website'
        ),
        Node(
            package='pkg_website_llm',
            namespace='LLM',
            executable='user_input_service',
            output='screen',
            name='user_input_sender'
        ),
        Node(
            package='pkg_website_llm',
            namespace='LLM',
            executable='feedback_website_llm',
            output='screen',
            name='feedbackwebsite'
        ),
        Node(
            package='pkg_website_llm',
            namespace='LLM',
            executable='pack_item_server',
            output='screen',
            name='pack_item_server'
        ),
        Node(
            package='pkg_website_llm',
            namespace='LLM',
            executable='image_saver',
            output='screen',
            name='saveImageFromODTF'
        ),             
    ])