"""Testing the database function"""
#pylint: disable=w0621

import pytest

import database
import medium

DEMO = medium.Medium("ID", "FILENAME", ["TAG1", "TAG2"])

@pytest.fixture(scope="function")
def data_base():
    """mock the database"""
    my_db = database.Database(":memory:")
    return my_db

def test_empty(data_base):
    """Empty database should return empty"""
    assert data_base.get_ids() == []

def test_put(data_base):
    """selecting all IDs if only one ID"""
    data_base.put(DEMO)
    result = data_base.database_cursor.execute("select medium_id from collection").fetchall()
    assert result == [("ID",)]

def test_select(data_base):
    """select a ID given that put worked"""
    data_base.put(DEMO)
    result = data_base.get_ids()
    assert result == [("ID",)]

def test_double(data_base):
    """Test if double values are prohibited"""
    data_base.put(DEMO)
    with pytest.raises(database.sqlite3.IntegrityError):
        data_base.put(DEMO)
