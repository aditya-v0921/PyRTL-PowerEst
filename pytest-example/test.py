# test.py
# Starter code — fill in the missing tests to fully verify app.py

import pytest
import app


def test_normalize_name_basic():
    # Example of a complete test:
    result = app.normalize_name("  alice   smith ")
    assert result == "Alice Smith"


def test_normalize_name_errors():
    # TODO: Write tests for invalid inputs, e.g. passing a non-string
    with pytest.raises(TypeError):
        app.normalize_name(123)
    # and an empty/whitespace-only string.
    with pytest.raises(ValueError):
        app.normalize_name("    ")
    # Hint: use pytest.raises(...)
    pass


def test_is_prime():
    # TODO: Write tests that check both prime and non-prime cases.
    #with pytest.raises():
    # Example cases: 2, 3, 4, 17, 0, -5
    pass


def test_safe_divide():
    # TODO: Write tests for:
    #   - normal division
    #   - divide by zero (should return None)
    #   - invalid types (should raise TypeError)
    pass


def test_compute_grade():
    # TODO: Write tests for grade calculation with and without dropping
    # the lowest score. Also test invalid inputs.
    pass


def test_find_median():
    # TODO: Write tests for odd and even lists and an empty list error.
    pass