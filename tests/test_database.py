import os
import pytest
from couchdb3_python.client import Client
from couchdb3_python.database import Database

COUCH = os.getenv("COUCHDB_URL")
USERNAME = os.getenv("COUCHDB_USERNAME")
PASSWORD = os.getenv("COUCHDB_PASSWORD")


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


def test_database_create_delete():
    client = Client(COUCH, username=USERNAME, password=PASSWORD)
    db = Database(client, "testdb2")

    # 既に存在していたら削除
    if db.exists():
        db.delete()

    # 作成
    resp = db.create()
    assert resp["ok"] is True

    # 存在確認
    assert db.exists() is True

    # 削除
    resp = db.delete()
    assert resp["ok"] is True

    # 削除後は存在しない
    assert db.exists() is False


@pytest.fixture
def db():
    client = Client(COUCH, username=USERNAME, password=PASSWORD)
    db = Database(client, "extended_test_db")

    if db.exists():
        db.delete()
    db.create()

    yield db

    if db.exists():
        db.delete()


def test_info(db):
    info = db.info()
    assert info["db_name"] == "extended_test_db"


def test_all_docs_empty(db):
    docs = db.all_docs()
    assert docs["total_rows"] == 0


def test_changes_empty(db):
    changes = db.changes()
    assert "results" in changes


def test_compact(db):
    resp = db.compact()
    assert resp["ok"] is True


def test_ensure_full_commit(db):
    resp = db.ensure_full_commit()
    assert resp["ok"] is True


def test_revs_diff(db):
    resp = db.revs_diff({"doc1": ["1-xxx"]})
    assert isinstance(resp, dict)


def test_missing_revs(db):
    resp = db.missing_revs({"doc1": ["1-xxx"]})
    assert isinstance(resp, dict)


def test_purge(db):
    # purge は通常 empty でも ok
    resp = db.purge({})
    assert isinstance(resp, dict)

