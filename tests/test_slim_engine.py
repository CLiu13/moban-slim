import os

from nose.tools import eq_
from moban.plugins import ENGINES, BaseEngine
from moban_slim.engine import EngineSlim


def test_slim_engine_type():
    engine = ENGINES.get_engine("slim", [], "")
    assert engine.engine_cls == EngineSlim
    pass


def test_slim_file_tests():
    output = "test.txt"
    path = os.path.join("tests", "fixtures", "slim_tests")
    engine = BaseEngine([path], path, EngineSlim)
    engine.render_to_file("file_tests.slim", "file_tests.json", output)
    with open(output, "r") as output_file:
        # In some versions of python, the attributes of the
        # meta tag on line 9 of file_tests.slim are flipped.
        # To fix this, we check for both cases.
        expected_path = os.path.join("tests", "fixtures", "slim_tests",
                                     "expected_output.txt")
        expected_path_2 = os.path.join("tests", "fixtures", "slim_tests",
                                       "expected_output_2.txt")
        with open(expected_path) as expected_file:
            with open(expected_path_2) as expected_file_2:
                expected = expected_file.read()
                expected_2 = expected_file_2.read()
                content = output_file.read()
                try:
                    eq_(content, expected)
                except AssertionError:
                    eq_(content, expected_2)
    os.unlink(output)


def test_slim_string_template():
    string_template = "{{ content }}"
    output = "test.txt"
    path = os.path.join("tests", "fixtures", "slim_tests")
    engine = BaseEngine([path], path, EngineSlim)
    engine.render_string_to_file(string_template, "file_tests.json", output)
    with open(output, "r") as output_file:
        expected = "my_content"
        content = output_file.read()
        eq_(content, expected)
    os.unlink(output)
