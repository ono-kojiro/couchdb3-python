from .client import Client
from .exceptions import NotFoundError
from urllib.parse import urlencode


class Database:
    """
    CouchDB のデータベースを表すクラス。
    基本操作 + 主要 API を提供する。
    """

    def __init__(self, client: Client, name: str):
        self.client = client
        self.name = name

    # ---------------------------
    # URL 生成
    # ---------------------------
    def url(self, path: str = "") -> str:
        """
        互換性維持のための URL 生成メソッド。
        """
        if path:
            return self.client.url(f"{self.name}/{path}")
        return self.client.url(self.name)
    
    def _path(self, suffix: str = "") -> str:
        if suffix:
            return f"{self.name}/{suffix}"
        return self.name

    # ---------------------------
    # 基本操作
    # ---------------------------

    def create(self) -> dict:
        return self.client.put(self.name)

    def delete(self) -> dict:
        return self.client.delete(self.name)

    def exists(self) -> bool:
        try:
            self.client.head(self.name)
            return True
        except NotFoundError:
            return False

    def put(self, docid: str, json: dict):
        return self.client.put(self._path(docid), json=json)

    # ---------------------------
    # 拡張 API
    # ---------------------------

    def info(self) -> dict:
        return self.client.get(self.name)

    def all_docs(self, **params) -> dict:
        return self.client.get(self._path("_all_docs"), params=params)

    def changes(self, params: dict | None = None) -> dict:
        return self.client.get(self._path("_changes"), params=params)

    def longpoll(self, since="now", params=None):
        query = {"feed": "longpoll", "since": since}
        if params:
            query.update(params)
        return self.client.get(self._path("_changes"), params=query)

    def compact(self):
        return self.client.post(self._path("_compact"), json={})

    def ensure_full_commit(self):
        return self.client.post(self._path("_ensure_full_commit"), json={})

    def purge(self, docs: dict):
        return self.client.post(self._path("_purge"), json=docs)

    def missing_revs(self, docs: dict):
        return self.client.post(self._path("_missing_revs"), json=docs)

    def revs_diff(self, docs: dict):
        return self.client.post(self._path("_revs_diff"), json=docs)

    def bulk(self, docs: list):
        return self.client.post(self._path("_bulk_docs"), json={"docs": docs})

    def find(self, query: dict):
        return self.client.post(self._path("_find"), json=query)

    def create_index(self, fields: list, name=None, index_type="json"):
        payload = {"index": {"fields": fields}, "type": index_type}
        if name:
            payload["name"] = name
        return self.client.post(self._path("_index"), json=payload)

    # ---------------------------
    # Design Document
    # ---------------------------

    def create_design_doc(self, name: str, views=None, shows=None, lists=None, updates=None):
        doc_id = f"_design/{name}"
        payload = {"_id": doc_id}

        if views:
            payload["views"] = views
        if shows:
            payload["shows"] = shows
        if lists:
            payload["lists"] = lists
        if updates:
            payload["updates"] = updates

        try:
            existing = self.client.get(self._path(doc_id))
            payload["_rev"] = existing["_rev"]
        except Exception:
            pass

        return self.put(doc_id, json=payload)

    def query_view(self, design: str, view: str, params=None):
        return self.client.get(self._path(f"_design/{design}/_view/{view}"), params=params)

    def show(self, design: str, show: str, docid: str, params=None):
        return self.client.get(self._path(f"_design/{design}/_show/{show}/{docid}"), params=params)

    def list(self, design: str, listname: str, view: str, params=None):
        return self.client.get(self._path(f"_design/{design}/_list/{listname}/{view}"), params=params)

    def update(self, design: str, update: str, docid=None, body=None):
        if docid:
            path = f"_design/{design}/_update/{update}/{docid}"
        else:
            path = f"_design/{design}/_update/{update}"
        return self.client.post(self._path(path), json=body)
