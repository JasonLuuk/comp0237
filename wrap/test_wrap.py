import json
import pytest


from wrap import wrap

with open("wrap.json") as data_file:
    testdata = [json.loads(line) for line in data_file]


@pytest.mark.parametrize("input_data,expected", testdata)
def test_wrap(input_data, expected):
    assert wrap(*input_data) == expected


@pytest.fixture(scope="session", autouse=True)
def starter(request):
    import time
    start_time = time.time()

    def finalizer():
        print("runtime: {}".format(str(time.time() - start_time)))

    request.addfinalizer(finalizer)
