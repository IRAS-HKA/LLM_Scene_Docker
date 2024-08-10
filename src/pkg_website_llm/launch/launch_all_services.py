from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
import os

def generate_launch_description():
    return LaunchDescription([
        # Node(
        #     package='pkg_website_llm',
        #     namespace='LLM',
        #     executable='param_setter',
        #     output='screen',
        #     name='Parameter_Setter'
        # ),        
        Node(
            package='pkg_website_llm',
            namespace='LLM',
            executable='website_llm',
            output='screen',
            name='website'
        ),
        # Node(
        #     package='pkg_llm_docker',
        #     namespace='LLM',
        #     executable='llm_action_server',
        #     output='screen',
        #     name='LLM1'
        # ),
        Node(
            package='pkg_website_llm',
            namespace='LLM',
            executable='user_input_service',
            output='screen',
            name='user_input_sender'
        ),
        # Node(
        #     package='pkg_website_llm',
        #     namespace='LLM',
        #     executable='feedback_website_llm',
        #     output='screen',
        #     name='feedbackwebsite'
        # ),
        Node(
            package='pkg_website_llm',
            namespace='LLM',
            executable='delete_parameter',
            output='screen',
            name='delete_parameter_service'
        )           


    ])