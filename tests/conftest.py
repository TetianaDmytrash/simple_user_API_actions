"""
    common fixtures
"""


import pytest


@pytest.fixture(autouse=True)
def common_setup():
    """
        common setup
    :return:
    """
    pass


@pytest.fixture(autouse=True)
def common_cleanup():
    """
        common cleanup
    :return:
    """
    # get all user
    # if len(all_user) not 0
    # clean
    pass
