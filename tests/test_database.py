import pytest
from couchdb3_python.client import Client
from couchdb3_python.database import Database


def test_database_url_basic():
    client = Client("http://localhost:5984")
    db = Database(client, "mydb")
    assert db.url() == "http://localhost:5984/mydb"


def test_database_url_with_path():
    client = Client("http://localhost:5984")
    db = Database(client, "mydb")
    assert db.url("_all_docs") == "http://localhost:5984/mydb/_all_docs"


def test_database_url_with_prefix():
    client = Client("http://localhost:5984/couchdb")
    db = Database(client, "mydb")
    assert db.url() == "http://localhost:5984/couchdb/mydb"


def test_database_url_with_prefix_and_path():
    client = Client("http://localhost:5984/couchdb")
    db = Database(client, "mydb")
    assert db.url("_all_docs") == "http://localhost:5984/couchdb/mydb/_all_docs"

