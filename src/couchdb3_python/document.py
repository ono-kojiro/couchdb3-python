from .client import Client
from .exceptions import NotFoundError


class Document:
    """
    CouchDB のドキュメントを表すクラス。
    まずは基本的な CRUD のみを実装する。
    """

    def __init__(self, client, dbname, docid, data=None):
        self.client = client
        self.dbname = dbname
        self.id = docid
        self.data = data or {}
        self.rev = self.data.get("_rev")

    # ---------------------------
    # URL 生成
    # ---------------------------

    def url(self) -> str:
        return self.client.url(f"{self.dbname}/{self.id}")

    # ---------------------------
    # CRUD 操作
    # ---------------------------

    def get(self) -> dict:
        """
        ドキュメントを取得する。
        GET /{db}/{id}
        """
        return self.client.get(f"{self.dbname}/{self.id}")

    def exists(self) -> bool:
        """
        ドキュメントが存在するか確認する。
        HEAD /{db}/{id}
        """
        try:
            self.client.head(f"{self.dbname}/{self.id}")
            return True
        except NotFoundError:
            return False

    def create(self, data: dict) -> dict:
        """
        ドキュメントを新規作成する。
        PUT /{db}/{id}
        """
        return self.client.put(f"{self.dbname}/{self.id}", json=data)

    def delete(self, rev: str) -> dict:
        """
        ドキュメントを削除する。
        DELETE /{db}/{id}?rev={rev}
        """
        path = f"{self.dbname}/{self.id}?rev={rev}"
        return self.client.delete(path)

    def fetch(self):
        resp = self.client.get(f"{self.dbname}/{self.id}")
        self.data = resp
        self.rev = resp.get("_rev")
        return self

    def save(self):
        self.data["_id"] = self.id

        if self.rev:
            self.data["_rev"] = self.rev
        else:
            self.data.pop("_rev", None)

        resp = self.client.put(f"{self.dbname}/{self.id}", json=self.data)

        if "rev" in resp:
            self.rev = resp["rev"]
            self.data["_rev"] = self.rev

        return resp
