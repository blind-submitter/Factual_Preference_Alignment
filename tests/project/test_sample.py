"""Sample test."""

import pytest

import src.project


@pytest.mark.integration_test()
def test_import():
    assert hasattr(src.project, "__name__")


# TODO: Replace this
def test_samplefn(my_test_number: int) -> None:
    """Test function."""
    assert my_test_number == 42
