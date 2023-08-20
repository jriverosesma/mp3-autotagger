import subprocess
import sys


def get_package_version(package_name: str) -> str | None:
    try:
        output = subprocess.check_output([sys.executable, "-m", "pip", "show", package_name])
        for line in output.decode().splitlines():
            if line.startswith("Version:"):
                return line.split(": ")[1]
    except subprocess.CalledProcessError:
        return None


def update_package(package_name: str = "mp3-autotagger") -> str:
    initial_version = get_package_version(package_name)
    if not initial_version:
        return f"Error: Unable to determine the current version of {package_name}. Make sure the package is installed"

    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package_name])
    except subprocess.CalledProcessError as e:
        return f"Error occurred while updating {package_name}. Error: {e}"

    updated_version = get_package_version(package_name)
    if not updated_version:
        return f"Error: Unable to determine the updated version of {package_name}."

    if initial_version == updated_version:
        return f"{package_name} is already at the latest version ({updated_version})."

    return f"{package_name} updated successfully from version {initial_version} to {updated_version}!"
