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

def test_mango_find_and_index():
    client, db = setup_db("mango_test_db")

    # データ投入
    db.put("u1", json={"name": "Alice", "age": 30})
    db.put("u2", json={"name": "Bob", "age": 25})
    db.put("u3", json={"name": "Charlie", "age": 40})

    # インデックス作成
    db.create_index(["age"], name="age-index")

    # Mango Query
    resp = db.find({
        "selector": {
            "age": {"$gt": 30}
        }
    })

    docs = resp["docs"]
    ids = [d["_id"] for d in docs]

    assert "u3" in ids
    assert "u1" not in ids
    assert "u2" not in ids

