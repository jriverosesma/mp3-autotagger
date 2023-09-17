import subprocess


def is_ffmpeg_installed():
    """
    Check if ffmpeg is installed on the system.

    Returns:
        bool: `True` if ffmpeg is installed, `False` otherwise.
    """

    try:
        result = subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            return True
        return False
    except FileNotFoundError:
        return False
