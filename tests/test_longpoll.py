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

def test_changes_longpoll():
    client, db = setup_db("changes_longpoll_db")

    # まず normal モードで last_seq を取得
    initial = db.changes()
    last = initial["last_seq"]

    # 別スレッドで更新する代わりに、先に PUT しておく
    db.put("doc1", json={"foo": 1})

    # longpoll は変更があるとすぐ返る
    resp = db.longpoll(since=last)

    assert "results" in resp
    assert len(resp["results"]) >= 1

