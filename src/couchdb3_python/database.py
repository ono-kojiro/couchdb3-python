from .client import Client
from .exceptions import NotFoundError


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
        if path:
            return self.client.url(f"{self.name}/{path}")
        return self.client.url(self.name)

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

    def put(self, docid, json):
        return self.client.put(f"{self.name}/{docid}", json=json)

    # ---------------------------
    # 拡張 API
    # ---------------------------

    def info(self) -> dict:
        """
        GET /{db}
        データベース情報を取得する。
        """
        return self.client.get(self.name)

    def all_docs(self, **params) -> dict:
        """
        GET /{db}/_all_docs
        params は ?key=xxx などのクエリに変換される。
        """
        query = self._encode_params(params)
        path = f"{self.name}/_all_docs{query}"
        return self.client.get(path)

    def changes(self, **params) -> dict:
        """
        GET /{db}/_changes
        """
        query = self._encode_params(params)
        path = f"{self.name}/_changes{query}"
        return self.client.get(path)

    #def compact(self) -> dict:
    #    """
    #    POST /{db}/_compact
    #    """
    #    return self.client.post(f"{self.name}/_compact", json=None)

    def compact(self):
        return self.client.post(f"{self.name}/_compact", json={})

    def ensure_full_commit(self) -> dict:
        """
        POST /{db}/_ensure_full_commit
        Content-Type: application/json
        Body: {}
        """
        return self.client.post(f"{self.name}/_ensure_full_commit", json={})

    def purge(self, docs: dict) -> dict:
        """
        POST /{db}/_purge
        docs = {"docid": ["rev1", "rev2"]}
        """
        return self.client.post(f"{self.name}/_purge", json=docs)

    def missing_revs(self, docs: dict) -> dict:
        """
        POST /{db}/_missing_revs
        """
        return self.client.post(f"{self.name}/_missing_revs", json=docs)

    def revs_diff(self, docs: dict) -> dict:
        """
        POST /{db}/_revs_diff
        """
        return self.client.post(f"{self.name}/_revs_diff", json=docs)

    # ---------------------------
    # 内部ユーティリティ
    # ---------------------------

    def _encode_params(self, params: dict) -> str:
        if not params:
            return ""
        from urllib.parse import urlencode
        return "?" + urlencode(params)

    def bulk(self, docs: list):
        """
        Bulk API: _bulk_docs による一括 insert/update
        docs は dict のリスト（_id, _rev を含んでいてもよい）
        """
        payload = {"docs": docs}
        return self.client.post(f"{self.name}/_bulk_docs", json=payload)

