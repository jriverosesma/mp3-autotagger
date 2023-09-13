import subprocess
import sys


def get_package_version(package_name: str) -> str | None:
    """
    Retrieve the installed version of a given package.

    Args:
        package_name (str): Name of the package whose version needs to be retrieved.

    Returns:
        str | None: The installed version of the package, or None if the package is not installed.
    """

    try:
        # Run the pip command to get package details
        output = subprocess.check_output([sys.executable, "-m", "pip", "show", package_name])

        # Search for the line that starts with "Version:"
        for line in output.decode().splitlines():
            if line.startswith("Version:"):
                return line.split(": ")[1]
    except subprocess.CalledProcessError:
        # If subprocess encounters an error, return None
        return None


def update_package(package_name: str = "mp3-autotagger") -> str:
    """
    Update the specified package to its latest version using pip.

    Args:
        package_name (str, optional): Name of the package to be updated. Defaults to "mp3-autotagger".

    Returns:
        str: A message indicating the result of the update attempt.
    """

    # Get the currently installed version of the package
    initial_version = get_package_version(package_name)

    if not initial_version:
        return f"Error: Unable to determine the current version of {package_name}. Make sure the package is installed."

    try:
        # Run the pip command to upgrade the package
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package_name])
    except subprocess.CalledProcessError as e:
        # If subprocess encounters an error during upgrade, return an error message
        return f"Error occurred while updating {package_name}. Error: {e}"

    # Get the version of the package after the upgrade
    updated_version = get_package_version(package_name)

    if not updated_version:
        # If unable to retrieve the updated version, return an error message
        return f"Error: Unable to determine the updated version of {package_name}."

    if initial_version == updated_version:
        # If the version remains the same after the upgrade, return a
        # message indicating the package is already up to date
        return f"{package_name} is already at the latest version ({updated_version})."

    # If the update was successful, return a success message
    return f"{package_name} updated successfully from version {initial_version} to {updated_version}!"
