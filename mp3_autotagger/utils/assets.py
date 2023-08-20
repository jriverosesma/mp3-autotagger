from importlib.resources import path as resource_path
from pathlib import Path


def get_resource_paths(package: str, *resource_names: str) -> dict[str, Path]:
    resource_paths: dict[str, Path] = {}

    for resource_name in resource_names:
        with resource_path(package, resource_name) as data_path:
            resource_paths[resource_name] = data_path

    return resource_paths


# Fetch all resource paths
resource_paths: dict[str, Path] = get_resource_paths(
    "mp3_autotagger", "main_icon.png", "autotagger_icon.png", "youtube2mp3_icon.png", "no_cover.jpg", "eng-es.qm"
)

# Access individual paths
main_icon_path: Path = resource_paths["main_icon.png"]
autotagger_icon_path: Path = resource_paths["autotagger_icon.png"]
youtube2mp3_icon_path: Path = resource_paths["youtube2mp3_icon.png"]
no_cover_path: Path = resource_paths["no_cover.jpg"]
translation_eng_es_path: Path = resource_paths["eng-es.qm"]