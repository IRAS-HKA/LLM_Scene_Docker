from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'pkg_website_llm'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
        (os.path.join('share', package_name, 'templates'), glob('pkg_website_llm/templates/*')),
        #(os.path.join('share', package_name, 'static'), glob('pkg_website_llm/static/*')),
        #(os.path.join('share', package_name, 'static/css/'), glob('pkg_website_llm/static/css/*')),

    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='robot',
    maintainer_email='drma1025@h-ka.de',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'website_llm = pkg_website_llm.website_llm:main',
            'feedback_website_llm = pkg_website_llm.WebsiteFeedbackService:main',   
            'user_input_service = pkg_website_llm.UserInputServiceSender:main',
            'param_setter = pkg_website_llm.ParamSetter:main',
            'param_getter = pkg_website_llm.ParamGetter:main',
            'delete_parameter = pkg_website_llm.DeleteParameterService:main',
            'pack_item_server = pkg_website_llm.PackItemServer:main',
            'image_saver = pkg_website_llm.LiveImageSubscriber:main',
        ],
    },
)
