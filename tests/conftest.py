from utility.util import MultiThreadCopier
import pytest


@pytest.fixture()
def multithreadcopier() -> MultiThreadCopier:
    return MultiThreadCopier()