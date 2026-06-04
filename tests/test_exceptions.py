import pytest
from couchdb3_python.exceptions import (
    CouchDBError,
    HTTPError,
    CouchDBResponseError,
    NotFoundError,
    ConflictError,
)


def test_http_error_message():
    err = HTTPError(404, "Not Found", url="http://localhost/db")
    assert "HTTP 404" in str(err)
    assert "Not Found" in str(err)
    assert "http://localhost/db" in str(err)


def test_couchdb_response_error_message():
    err = CouchDBResponseError("not_found", "missing", status=404, url="/db")
    assert "not_found" in str(err)
    assert "missing" in str(err)
    assert "HTTP 404" in str(err)
    assert "/db" in str(err)


def test_not_found_error_is_subclass():
    err = NotFoundError("not_found", "missing")
    assert isinstance(err, CouchDBResponseError)
    assert isinstance(err, CouchDBError)


def test_conflict_error_is_subclass():
    err = ConflictError("conflict", "Document update conflict")
    assert isinstance(err, CouchDBResponseError)
    assert isinstance(err, CouchDBError)

