import pytest

from mp3_autotagger.utils.package import get_package_version, update_package


@pytest.fixture(scope="class")
def package_name() -> str:
    return "mp3-autotagger"


def test_update_package(package_name: str) -> None:
    initial_version = get_package_version(package_name)
    status = update_package()
    updated_version = get_package_version(package_name)

    if initial_version is None:
        assert (
            status
            == f"Error: Unable to determine the current version of {package_name}. Make sure the package is installed"
        )
    elif updated_version == initial_version:
        assert status == f"{package_name} is already at the latest version ({updated_version})."
    else:
        assert status == f"{package_name} updated successfully from version {initial_version} to {updated_version}!"
