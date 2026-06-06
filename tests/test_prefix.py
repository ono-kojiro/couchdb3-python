import pytest
import os
from dotenv import load_dotenv
from couchdb3_python.client import Client

# .env を読み込む
load_dotenv()

API_KEY = os.getenv("API_KEY")
HEADERS = {"X-API-Key": API_KEY}


@pytest.fixture
def client():
    return Client(
        base_url="https://localhost/couchdb",
        timeout=5.0,
        verify=False,
    )


def test_prefix_all_dbs(client):
    resp = client.get("/_all_dbs", headers=HEADERS)
    assert isinstance(resp, list)


def test_prefix_create_db(client):
    dbname = "mydb"

    try:
        client.delete(f"/{dbname}", headers=HEADERS)
    except Exception:
        pass

    resp = client.put(f"/{dbname}", headers=HEADERS)
    assert resp["ok"] is True

    dbs = client.get("/_all_dbs", headers=HEADERS)
    assert dbname in dbs


def test_prefix_put_and_get_doc(client):
    dbname = "mydb"

    resp = client.post(
        f"/{dbname}",
        json={"hello": "world"},
        headers=HEADERS,
    )
    assert resp["ok"] is True
    doc_id = resp["id"]

    fetched = client.get(f"/{dbname}/{doc_id}", headers=HEADERS)
    assert fetched["hello"] == "world"
