from .client import Client


class Database:
    """
    CouchDB のデータベースを表すクラス。
    まずは URL の生成のみを担当する。
    """
    def __init__(self, client: Client, name: str):
        self.client = client
        self.name = name

    def url(self, path: str = "") -> str:
        """
        データベースの URL を返す。
        path が指定されれば /{db}/{path} となる。
        """
        if path:
            return self.client.url(f"{self.name}/{path}")
        return self.client.url(self.name)

