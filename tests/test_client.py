import pytest
from couchdb3_python.client import Client
from couchdb3_python.exceptions import NotFoundError

from dotenv import load_dotenv
import os

load_dotenv()

COUCH = os.getenv("COUCHDB_URL")
username = os.getenv("COUCHDB_USERNAME")
password = os.getenv("COUCHDB_PASSWORD")

def test_client_url_basic():
    c = Client("http://localhost:5984")
    assert c.url("mydb") == "http://localhost:5984/mydb"


def test_client_url_with_prefix():
    c = Client("http://localhost:5984/couchdb")
    assert c.url("mydb") == "http://localhost:5984/couchdb/mydb"


def test_client_url_with_prefix_and_slash():
    c = Client("http://localhost:5984/couchdb/")
    assert c.url("mydb") == "http://localhost:5984/couchdb/mydb"


def test_client_url_absolute_path():
    c = Client("http://localhost:5984")
    assert c.url("/_all_dbs") == "http://localhost:5984/_all_dbs"


def test_client_url_double_slash_not_generated():
    c = Client("http://localhost:5984/couchdb/")
    assert c.url("/mydb") == "http://localhost:5984/couchdb/mydb"


def test_head_not_found():
    client = Client(COUCH, username=username, password=password)
    with pytest.raises(NotFoundError):
        client.head("db_that_does_not_exist")


def test_put_and_delete_database():
    client = Client(COUCH, username=username, password=password)

    # データベース作成
    resp = client.put("testdb")
    assert resp["ok"] is True

    # データベース削除
    resp = client.delete("testdb")
    assert resp["ok"] is True

