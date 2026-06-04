import os
from dotenv import load_dotenv

from couchdb3_python.client import Client
from couchdb3_python.database import Database

load_dotenv()

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

def test_changes_normal_mode():
    client, db = setup_db("changes_test_db")

    # ドキュメントを追加
    db.put("doc1", json={"foo": 1})
    db.put("doc2", json={"bar": 2})

    resp = db.changes()

    assert "results" in resp
    assert "last_seq" in resp
    assert len(resp["results"]) >= 2

