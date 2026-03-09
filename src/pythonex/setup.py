from setuptools import find_packages, setup

package_name = 'pythonex'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ahmed',
    maintainer_email='ahmed@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        'simple_par= pythonex.simple_par : main',
        "simple_service= pythonex.simple_server : main",
        "simple_client= pythonex.simple_client : main" ,
        ], 
    },
)
