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

def test_changes_since_persistence():
    client, db = setup_db("changes_since_db")

    # 初回：ドキュメントを2つ作成
    db.put("doc1", json={"a": 1})
    db.put("doc2", json={"b": 2})

    # 1. 初回の changes を取得
    resp1 = db.changes()
    last_seq = resp1["last_seq"]

    # 2. "永続化"（テストでは変数に保存するだけ）
    saved_last_seq = last_seq

    # 3. 追加の変更を行う
    db.put("doc3", json={"c": 3})

    # 4. since を使って差分だけ取得
    resp2 = db.changes({"since": saved_last_seq})

    # 差分には doc3 の変更だけが含まれるはず
    ids = [r["id"] for r in resp2["results"]]

    assert "doc3" in ids
    assert "doc1" not in ids
    assert "doc2" not in ids

