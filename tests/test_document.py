import os
import pytest
from couchdb3_python.client import Client
from couchdb3_python.database import Database
from couchdb3_python.document import Document


COUCH = os.getenv("COUCHDB_URL")
USERNAME = os.getenv("COUCHDB_USERNAME")
PASSWORD = os.getenv("COUCHDB_PASSWORD")


def test_document_crud():
    client = Client(COUCH, username=USERNAME, password=PASSWORD)
    db = Database(client, "doc_test_db")

    # DB が存在していたら削除
    if db.exists():
        db.delete()

    db.create()

    doc = Document(client, "doc_test_db", "doc1")

    # 存在しない
    assert doc.exists() is False

    # 作成
    resp = doc.create({"name": "Alice"})
    assert resp["ok"] is True
    rev = resp["rev"]

    # 存在する
    assert doc.exists() is True

    # 取得
    data = doc.get()
    assert data["name"] == "Alice"

    # 削除
    resp = doc.delete(rev)
    assert resp["ok"] is True

    # 削除後は存在しない
    assert doc.exists() is False

    # DB 削除
    db.delete()

