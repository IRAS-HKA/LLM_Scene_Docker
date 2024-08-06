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
            'website_llm = pkg_website_llm.website_llm:main'            
        ],
    },
)
