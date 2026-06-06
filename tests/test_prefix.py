import pytest
from couchdb3_python.client import Client

API_KEY = "KEY_ABC123"


@pytest.fixture
def client():
    return Client(
        base_url="https://localhost/couchdb",
        timeout=5.0,
        verify=False,   # ← これが重要
    )


def test_prefix_all_dbs(client):
    resp = client.get(
        "/_all_dbs",
        headers={"X-API-Key": API_KEY},
    )
    assert isinstance(resp, list)


def test_prefix_create_db(client):
    dbname = "mydb"

    try:
        client.delete(f"/{dbname}", headers={"X-API-Key": API_KEY})
    except Exception:
        pass

    resp = client.put(f"/{dbname}", headers={"X-API-Key": API_KEY})
    assert resp["ok"] is True

    dbs = client.get("/_all_dbs", headers={"X-API-Key": API_KEY})
    assert dbname in dbs


def test_prefix_put_and_get_doc(client):
    dbname = "mydb"

    resp = client.post(
        f"/{dbname}",
        json={"hello": "world"},
        headers={"X-API-Key": API_KEY},
    )
    assert resp["ok"] is True
    doc_id = resp["id"]

    fetched = client.get(
        f"/{dbname}/{doc_id}",
        headers={"X-API-Key": API_KEY},
    )
    assert fetched["hello"] == "world"
