import pytest
import time
from load_testdata import load_json_testcases

if pytest.use_correct:
    from correct_python_programs.sieve import sieve
else:
    from sieve import sieve


testdata = load_json_testcases(sieve.__name__)


@pytest.mark.parametrize("input_data,expected", testdata)
def test_sieve(input_data, expected):
    assert sieve(*input_data) == expected

@pytest.fixture(scope="session", autouse=True)
def starter(request):
    start_time = time.time()

    def finalizer():
        print("runtime: {}".format(str(time.time() - start_time)))

    request.addfinalizer(finalizer)