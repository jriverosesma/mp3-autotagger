from importlib.resources import files
from pathlib import Path


def get_resource_paths(package: str, *resource_relative_paths: str) -> dict[str, Path]:
    """
    Fetch the file paths of multiple resources from a specified package.

    Args:
        package (str): Name of the package containing the resources.
        *resource_names (str): Resources (files) relative path to package folder.

    Returns:
        dict[str, Path]: Dictionary mapping resource names to their respective file paths.
    """

    resource_paths: dict[str, Path] = {}
    package_resources = files(package)

    for r_path in resource_relative_paths:
        # Fetch and store the path for each resource
        resource_paths[Path(r_path).name] = package_resources / r_path

    return resource_paths


# Fetch all resource paths
RESOURCE_PATHS: dict[str, Path] = get_resource_paths(
    "mp3_autotagger",
    "assets/main_icon.png",
    "assets/autotagger_icon.png",
    "assets/youtube2mp3_icon.png",
    "assets/no_cover.jpg",
    "translations/eng-es.qm",
)
