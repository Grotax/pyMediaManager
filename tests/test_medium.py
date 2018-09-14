"""Testing the medium function"""
#pylint: disable=w0621

import json

import pytest

from mediamanager import medium


DEMO = medium.Medium("ID", "FILENAME", json.dumps(["TAG1", "TAG2"]))
DEMO2 = medium.Medium("ID2", "FILENAME2", json.dumps(["TAG1", "TAG2"]))

ID1 = "ID"
FILENAME1 = "FILENAME"
TAGS1 = ["TAG1", "TAG2"]
ID2 = "ID2"
FILENAME2 = "FILENAME2"
TAGS2 = ["TAG2", "TAG3"]

@pytest.fixture(scope="function")
def demo():
    """first demo"""
    return medium.Medium(ID1, FILENAME1, json.dumps(TAGS1))

@pytest.fixture(scope="function")
def demo2():
    """second demo"""
    return medium.Medium(ID2, FILENAME2, json.dumps(TAGS2))

def test___str__(demo, demo2):
    """test magic string function"""
    assert str(demo) == demo.filename
    assert str(demo) != demo2.filename
    assert str(demo2) == demo2.filename
    assert str(demo2) != demo.filename

def test___repr__(demo, demo2):
    """test self-reproducing repr"""
    assert repr(demo) == """medium.Medium('ID', 'FILENAME', '["TAG1", "TAG2"]')"""
    assert repr(demo2) == """medium.Medium('ID2', 'FILENAME2', '["TAG2", "TAG3"]')"""
    # assert DEMO == eval(repr(DEMO))

def test___eq__():
    """equality test"""
    first = medium.Medium("ID", "FILENAME", json.dumps(["TAG1", "TAG2"]))
    second = medium.Medium("ID", "FILENAME", json.dumps(["TAG1", "TAG2"]))
    third = medium.Medium("ID", "FILENAME", json.dumps(["TAG1", "TAG111"]))
    assert first == second
    assert first != third
    assert second != third


def test_mime_type():
    """brauchen dafür vielleicht testdatei"""
    pass

def test_rename():
    """verändert dateiname auf fs, mock?"""
    pass

def test_load_tags():
    """Changes medium object"""
    pass

def test_add_tags():
    """adding tags to medium"""
    pass

def test_get_tags():
    """json"""
    assert DEMO.get_tags() == json.dumps(DEMO.tags)

def test_contains(demo, demo2):
    """check if tags are there"""
    assert demo.contains("TAG1")
    assert demo.contains("TAG2")
    assert not demo.contains("TAG3")
    assert not demo2.contains("TAG1")
    assert demo2.contains("TAG2")
    assert demo2.contains("TAG3")

def test_delete_tag(demo):
    """deleta  tag show if really gone"""
    assert demo.contains("TAG1")
    demo.delete_tag("TAG1")
    assert not demo.contains("TAG1")

def test_create_media_id():
    """also needs a file"""
    pass
