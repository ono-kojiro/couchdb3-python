from .urlresolver import URLResolver


class Client:
    """
    CouchDB への接続を表す最小クライアント。
    まずは URLResolver を使った URL 生成のみを実装する。
    """
    def __init__(self, base_url: str):
        self.resolver = URLResolver(base_url)

    def url(self, path: str) -> str:
        """
        指定されたパスを完全な URL に変換する。
        HTTP 通信はまだ実装しない。
        """
        return self.resolver.resolve(path)

