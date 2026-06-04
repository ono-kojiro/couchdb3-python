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

def test_mapreduce_basic():
    client, db = setup_db("mapreduce_test_db")

    # データ投入
    db.put("u1", json={"name": "Alice", "age": 30})
    db.put("u2", json={"name": "Bob", "age": 30})
    db.put("u3", json={"name": "Charlie", "age": 40})

    # Design Document 作成
    views = {
        "by_age": {
            "map": """
                function(doc) {
                    if (doc.age) emit(doc.age, 1);
                }
            """,
            "reduce": "_count"
        }
    }
    db.create_design_doc("users", views)

    # View 実行
    resp = db.query_view("users", "by_age", {"group": "true"})

    rows = resp["rows"]
    result = {row["key"]: row["value"] for row in rows}

    assert result[30] == 2
    assert result[40] == 1

