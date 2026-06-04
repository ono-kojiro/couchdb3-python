import os
from couchdb3_python.client import Client
from couchdb3_python.database import Database
from couchdb3_python.document import Document

COUCH = os.getenv("COUCHDB_URL")
USERNAME = os.getenv("COUCHDB_USERNAME")
PASSWORD = os.getenv("COUCHDB_PASSWORD")

def setup_db(name):
    client = Client(COUCH, username=USERNAME, password=PASSWORD)
    db = Database(client, name)
    if db.exists():
        db.delete()
    db.create()
    return client, db

def test_document_partial_update():
    client, db = setup_db("update_test_db")

    # 初期作成
    doc = Document(client, "update_test_db", "user1", {"name": "Alice", "age": 20})
    resp1 = doc.save()
    rev1 = resp1["rev"]

    # 部分更新
    resp2 = doc.update({"age": 21})
    rev2 = resp2["rev"]

    # rev が更新されている
    assert rev1 != rev2

    # 値が更新されている
    doc.fetch()
    assert doc.data["age"] == 21
    assert doc.data["name"] == "Alice"

