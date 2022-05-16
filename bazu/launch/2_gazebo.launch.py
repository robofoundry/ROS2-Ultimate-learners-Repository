import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import SetEnvironmentVariable



def generate_launch_description():
    # to resolve the stl files referred in urdf - set GAZEBO_MODEL_PATH first by adding
    # package share dir to path and then setting the env variable
    package_dir = get_package_share_directory('bazu')
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    urdf = os.path.join(package_dir,'bazu_gazebo.urdf')

    if 'GAZEBO_MODEL_PATH' in os.environ:
        model_path =  os.environ['GAZEBO_MODEL_PATH'] + ':' + package_dir
    else:
        model_path =  package_dir
    
    with open(urdf, 'r') as infp:
        robot_desc = infp.read()

    robot_state_pub = Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': robot_desc}],
            arguments=[urdf])
    
    exec_ros_factory = ExecuteProcess(
            cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_factory.so'],
            output='screen')

    spawn_entity =    Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            name='urdf_spawner',
            output='screen',
            arguments=["-topic", "/robot_description", "-entity", "bazu"])

    
    return LaunchDescription([
        SetEnvironmentVariable(name='GAZEBO_MODEL_PATH', value=model_path),
        robot_state_pub,
        exec_ros_factory,
        spawn_entity,
    ])

