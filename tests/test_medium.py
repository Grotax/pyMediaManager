"""Testing the medium function"""
#pylint: disable=w0621

import os
import json

import pytest

from mediamanager import medium

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
    first = medium.Medium("ID", "FILENAME", json.dumps(TAGS1))
    second = medium.Medium("ID", "FILENAME", json.dumps(TAGS1))
    third = medium.Medium("ID", "FILENAME", json.dumps(["TAG1", "TAG111"]))
    assert first == second
    assert first != third
    assert second != third

def test_mime_type(tmpdir):
    """brauchen dafür vielleicht testdatei"""
    path = lambda x: os.path.join(tmpdir, x)
    open(path("empty.txt"), "w").close()
    with open(path("text.txt"), "w") as file:
        file.write("Demo Text")
    with open(path("pixel.png"), "wb") as file:
        file.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR')
    media1 = medium.Medium(None, path("text.txt"), '["Text"]')
    media2 = medium.Medium(None, path("empty.txt"), '["Nothing"]')
    media3 = medium.Medium(None, path("pixel.png"), '["image"]')
    assert media1.mime_type() == "text/plain"
    assert media2.mime_type() == "inode/x-empty"
    assert media3.mime_type() == "image/png"

def test_rename(tmpdir):
    """change file name. can also change path"""
    path = lambda *x: os.path.join(tmpdir, *x)
    open(path("empty.txt"), "w").close()
    media = medium.Medium(None, path("empty.txt"), '["Nothing"]')
    media.rename(path("lol.txt"))
    assert os.listdir(tmpdir) == ["lol.txt"]
    os.mkdir(path("test"))
    media.rename(path("test", "lol.txt"))
    assert os.listdir(path("test")) == ["lol.txt"]

def test_load_tags(demo):
    """Changes medium object"""
    assert demo.tags == TAGS1
    assert demo.tags != ["Tag4"]
    demo.load_tags('["Tag4"]')
    assert demo.tags == ["Tag4"]
    assert demo.tags != TAGS1

def test_add_tags(demo):
    """adding tags to medium"""
    assert not demo.contains("TAG3")
    demo.add_tags("TAG3")
    assert demo.contains("TAG3")

def test_get_tags(demo):
    """tags as json test"""
    assert demo.get_tags() == json.dumps(TAGS1)

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

def test_create_media_id(tmpdir):
    """also needs a file"""
    path = lambda *x: os.path.join(tmpdir, *x)
    with open(path("pixel.png"), "wb") as file:
        file.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR')
    media = medium.Medium(None, path("pixel.png"), [])
    assert media.medium_id == \
    "02a3e298f1533f62558c58e4c70edcab9af5a50d62d925fd5390942020fb0fb8"
