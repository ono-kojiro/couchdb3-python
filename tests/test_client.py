import pytest
from couchdb3_python.client import Client


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

