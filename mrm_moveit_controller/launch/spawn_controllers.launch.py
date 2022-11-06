from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launches import generate_spawn_controllers_launch


def generate_launch_description():
    moveit_config = MoveItConfigsBuilder("mrm_001", package_name="mrm_moveit_controller").to_moveit_configs()
    return generate_spawn_controllers_launch(moveit_config)
