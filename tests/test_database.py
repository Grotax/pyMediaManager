"""Testing the database function"""
#pylint: disable=w0621

import copy
import json

import pytest

from mediamanager import database
from mediamanager import medium

DEMO = medium.Medium("ID", "FILENAME", json.dumps(["TAG1", "TAG2"]))
DEMO2 = medium.Medium("ID2", "FILENAME2", json.dumps(["TAG1", "TAG2"]))

@pytest.fixture(scope="function")
def data_base():
    """mock the database"""
    my_db = database.Database(":memory:")
    yield my_db
    my_db.database.close()

def test_empty(data_base):
    """Empty database should return empty"""
    result = data_base.database_cursor.execute(
        "select * from collection").fetchall()
    assert result == []
    assert data_base.get_ids() == []

def test_put(data_base):
    """selecting all IDs if only one ID"""
    data_base.put(DEMO)
    result = data_base.database_cursor.execute(
        "select * from collection").fetchall()
    assert result == [(DEMO.medium_id, DEMO.filename, DEMO.get_tags())]

def test_put_multiple(data_base):
    """test multiple puts"""
    data_base.put([DEMO, DEMO2])
    result = data_base.database_cursor.execute(
        "select medium_id from collection").fetchall()
    assert result == [(DEMO.medium_id,), (DEMO2.medium_id,)]

def test_ids(data_base):
    """select a ID, given that put works"""
    data_base.put(DEMO)
    result = data_base.get_ids()
    assert result == [(DEMO.medium_id,)]
    data_base.put(DEMO2)
    result = data_base.get_ids()
    assert result == [(DEMO.medium_id,), (DEMO2.medium_id,)]

def test_get(data_base):
    """tests the get function"""
    data_base.put(DEMO)
    data_base.put(DEMO2)
    result = data_base.get(DEMO.medium_id)
    assert result == [(DEMO.medium_id, DEMO.filename, DEMO.get_tags())]
    result = data_base.get(DEMO2.medium_id)
    assert result == [(DEMO2.medium_id, DEMO2.filename, DEMO2.get_tags())]

def test_get_all(data_base):
    """test the get all function"""
    data_base.put(DEMO)
    result = data_base.get_all()
    assert result == [(DEMO.medium_id, DEMO.filename, DEMO.get_tags())]
    data_base.put(DEMO2)
    result = data_base.get_all()
    assert result == [(DEMO.medium_id, DEMO.filename, DEMO.get_tags()),
                      (DEMO2.medium_id, DEMO2.filename, DEMO2.get_tags())]


def test_double(data_base):
    """Test if double values are prohibited"""
    data_base.put(DEMO)
    with pytest.raises(database.sqlite3.IntegrityError):
        data_base.put(DEMO)

def test_delete(data_base):
    """test a deletion"""
    data_base.put(DEMO)
    data_base.delete(DEMO.medium_id)
    assert data_base.get_ids() == []

def test_update(data_base):
    """test an update"""
    data_base.put(DEMO)
    manipulated = copy.deepcopy(DEMO)
    manipulated.filename += "1"
    data_base.update(manipulated)
    result = data_base.database_cursor.execute(
        "select filename from collection").fetchall()
    assert result[0][0] == manipulated.filename
    assert result[0][0] != DEMO.filename
    assert len(result) == 1
