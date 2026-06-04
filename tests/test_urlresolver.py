import pytest
from couchdb3_python.urlresolver import URLResolver


def test_basic_resolution():
    r = URLResolver("http://localhost:5984")
    assert r.resolve("mydb") == "http://localhost:5984/mydb"


def test_resolution_with_leading_slash():
    r = URLResolver("http://localhost:5984")
    assert r.resolve("/mydb") == "http://localhost:5984/mydb"


def test_base_url_with_trailing_slash():
    r = URLResolver("http://localhost:5984/")
    assert r.resolve("mydb") == "http://localhost:5984/mydb"


def test_base_url_with_prefix():
    r = URLResolver("http://localhost:5984/couchdb")
    assert r.resolve("mydb") == "http://localhost:5984/couchdb/mydb"


def test_base_url_with_prefix_and_slash():
    r = URLResolver("http://localhost:5984/couchdb/")
    assert r.resolve("mydb") == "http://localhost:5984/couchdb/mydb"


def test_absolute_path():
    r = URLResolver("http://localhost:5984/couchdb")
    assert r.resolve("/_all_dbs") == "http://localhost:5984/couchdb/_all_dbs"


def test_double_slash_is_not_generated():
    r = URLResolver("http://localhost:5984/couchdb/")
    assert r.resolve("/mydb") == "http://localhost:5984/couchdb/mydb"

