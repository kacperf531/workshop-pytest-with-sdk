from foo import multiply
import pytest

@pytest.mark.parametrize('a,b,exp_value', [(3,2,6), (4,2,8), (6,9,54)])
def test_multiply(a,b,exp_value):
    if a == 4:
        pytest.xfail('This is a bug, we don\'t know how multiply 4 yet.')
    assert multiply(a,b) == exp_value



