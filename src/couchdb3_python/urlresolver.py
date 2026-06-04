from urllib.parse import urljoin

class URLResolver:
    def __init__(self, base_url: str):
        # 末尾スラッシュを除去（ただし "http://host/" は残す）
        self.base_url = base_url.rstrip("/")

    def resolve(self, path: str) -> str:
        """
        base_url に prefix が含まれていても正しく結合する。
        path が絶対パスでも正しく扱う。
        """
        # path の先頭スラッシュは任意に許容する
        path = path.lstrip("/")

        # urljoin は prefix-aware で、二重スラッシュも防ぐ
        return urljoin(self.base_url + "/", path)

