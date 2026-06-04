from .client import Client
from .exceptions import NotFoundError


class Document:
    """
    CouchDB のドキュメントを表すクラス。
    まずは基本的な CRUD のみを実装する。
    """

    def __init__(self, client: Client, dbname: str, doc_id: str):
        self.client = client
        self.dbname = dbname
        self.id = doc_id

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

