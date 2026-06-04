import os
import pytest
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

def test_rev_updates_after_save():
    client, db = setup_db("rev_test_db")

    doc = Document(client, "rev_test_db", "doc1", {"foo": 1})
    resp1 = doc.save()
    rev1 = resp1["rev"]

    doc.data["foo"] = 2
    resp2 = doc.save()
    rev2 = resp2["rev"]

    assert rev1 != rev2
    assert doc.rev == rev2

def test_rev_updates_after_fetch():
    client, db = setup_db("rev_fetch_db")

    doc = Document(client, "rev_fetch_db", "doc1", {"foo": 10})
    resp1 = doc.save()
    rev1 = resp1["rev"]

    doc2 = Document(client, "rev_fetch_db", "doc1")
    doc2.fetch()

    assert doc2.rev == rev1

    doc2.data["foo"] = 20
    resp2 = doc2.save()
    rev2 = resp2["rev"]

    assert rev1 != rev2
    assert doc2.rev == rev2

