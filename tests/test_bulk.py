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

def test_bulk_insert_and_update():
    client, db = setup_db("bulk_test_db")

    # 1. 一括 insert
    docs = [
        {"_id": "user1", "name": "Alice"},
        {"_id": "user2", "name": "Bob"},
    ]
    resp1 = db.bulk(docs)

    # 成功した _rev を取得
    revs = {r["id"]: r["rev"] for r in resp1}

    assert "user1" in revs
    assert "user2" in revs

    # 2. 一括 update
    docs2 = [
        {"_id": "user1", "_rev": revs["user1"], "name": "Alice2"},
        {"_id": "user2", "_rev": revs["user2"], "name": "Bob2"},
    ]
    resp2 = db.bulk(docs2)

    revs2 = {r["id"]: r["rev"] for r in resp2}

    assert revs["user1"] != revs2["user1"]
    assert revs["user2"] != revs2["user2"]

