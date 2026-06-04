# couchdb3-python

`couchdb3-python` is a lightweight and practical Python client library for Apache CouchDB 3.x.  
It provides a clean, modern interface for working with CouchDB features such as CRUD operations,  
Bulk API, Changes API, Mango Query, MapReduce (Views), and Design Document handlers  
including **show**, **list**, and **update**.

This project was developed with reference to the original `couchdb3` library:

👉 https://github.com/N-Vlahovic/couchdb3

In addition, parts of this implementation were created **in collaboration with Microsoft Copilot (AI)**.  
While AI assistance was used to accelerate development and improve design clarity,  
all code was manually reviewed, validated, and adapted to ensure correctness, maintainability,  
and practical usability.

---

## Features

- Python 3.10+
- CRUD operations (`get`, `put`, `delete`)
- Bulk API
- Changes API (normal and longpoll)
- Mango Query (`_find`, `_index`)
- MapReduce (Design Documents / Views)
- Support for `show`, `list`, and `update` handlers
- Automatic `_rev` handling for design document updates
- Simple and explicit HTTP client built on `httpx`
- Fully testable architecture

---

## Installation

(To be added depending on distribution method)

---

## Usage Examples

### Database operations

```python
from couchdb3_python.client import Client
from couchdb3_python.database import Database

client = Client("http://localhost:5984", username="admin", password="password")
db = Database(client, "example")
db.create()
```

### Mango Query

```python
db.create_index(["age"])
docs = db.find({"selector": {"age": {"$gt": 20}}})
```

### MapReduce (View)

```python
views = {
    "by_age": {
        "map": "function(doc){ if(doc.age) emit(doc.age, 1); }",
        "reduce": "_count"
    }
}

db.create_design_doc("users", views=views)
rows = db.query_view("users", "by_age", {"group": "true"})
```

### show / list / update handlers

```python
shows = {
    "html": "function(doc, req){ return '<h1>' + doc.name + '</h1>'; }"
}

db.create_design_doc("users", shows=shows)
html = db.show("users", "html", "user1")
```



## Development Notes
This library was built with the following goals:

- Provide a clean and Pythonic interface to CouchDB 3.x
- Support the full range of CouchDB server-side features
- Enable design documents to be managed programmatically
- Offer a modern alternative to existing CouchDB Python clients

The implementation draws inspiration from the couchdb3 project
while being independently designed and rewritten with AI-assisted development.

