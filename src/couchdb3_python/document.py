from .client import Client
from .exceptions import NotFoundError


class Document:
    def __init__(self, client: Client, dbname: str, docid: str, data=None):
        self.client = client
        self.dbname = dbname
        self.id = docid
        self.data = data or {}
        self.rev = self.data.get("_rev")

    def _path(self) -> str:
        return f"{self.dbname}/{self.id}"

    def url(self) -> str:
        return self.client.url(self._path())

    def get(self) -> dict:
        return self.client.get(self._path())

    def exists(self) -> bool:
        try:
            self.client.head(self._path())
            return True
        except NotFoundError:
            return False

    def create(self, data: dict) -> dict:
        return self.client.put(self._path(), json=data)

    def delete(self, rev: str) -> dict:
        return self.client.delete(f"{self._path()}?rev={rev}")

    def fetch(self):
        resp = self.client.get(self._path())
        self.data = resp
        self.rev = resp.get("_rev")
        return self

    def save(self):
        self.data["_id"] = self.id

        if self.rev:
            self.data["_rev"] = self.rev
        else:
            self.data.pop("_rev", None)

        resp = self.client.put(self._path(), json=self.data)

        if "rev" in resp:
            self.rev = resp["rev"]
            self.data["_rev"] = self.rev

        return resp

    def update(self, fields: dict):
        self.fetch()
        self.data.update(fields)
        return self.save()
