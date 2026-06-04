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


def test_show_handler():
    client, db = setup_db("test_show_db")

    # データ投入
    db.put("u1", json={"name": "Alice", "age": 30})

    # show handler を含む design doc
    shows = {
        "html": """
            function(doc, req) {
                if (!doc) return "not found";
                return "<h1>" + doc.name + "</h1>";
            }
        """
    }

    db.create_design_doc("users", shows=shows)

    # 実行
    resp = db.show("users", "html", "u1")

    assert "<h1>Alice</h1>" in resp


def test_list_handler():
    client, db = setup_db("test_list_db")

    # データ投入
    db.put("u1", json={"name": "Alice", "age": 30})
    db.put("u2", json={"name": "Bob", "age": 25})

    # View + list handler
    views = {
        "by_age": {
            "map": """
                function(doc) {
                    if (doc.age) emit(doc.age, doc);
                }
            """
        }
    }

    lists = {
        "csv": """
            function(head, req) {
                start({"headers": {"Content-Type": "text/plain"}});
                var row;
                send("name,age\\n");
                while (row = getRow()) {
                    send(row.value.name + "," + row.value.age + "\\n");
                }
            }
        """
    }

    db.create_design_doc("users", views=views, lists=lists)

    # list handler 実行
    resp = db.list("users", "csv", "by_age")

    assert "name,age" in resp
    assert "Alice,30" in resp
    assert "Bob,25" in resp
