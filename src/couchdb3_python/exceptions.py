class CouchDBError(Exception):
    """
    CouchDB クライアントの基底例外クラス。
    すべての例外はこれを継承する。
    """
    pass


class HTTPError(CouchDBError):
    """
    HTTP レベルのエラー（ステータスコード付き）。
    """
    def __init__(self, status: int, message: str = "", *, url: str | None = None):
        self.status = status
        self.message = message
        self.url = url
        super().__init__(f"HTTP {status}: {message} ({url})")


class CouchDBResponseError(CouchDBError):
    """
    CouchDB が返す JSON エラー（error, reason を持つ）。
    """
    def __init__(self, error: str, reason: str, *, status: int | None = None, url: str | None = None):
        self.error = error
        self.reason = reason
        self.status = status
        self.url = url
        msg = f"{error}: {reason}"
        if status:
            msg = f"HTTP {status} - " + msg
        if url:
            msg += f" ({url})"
        super().__init__(msg)


class NotFoundError(CouchDBResponseError):
    """404: データベースまたはドキュメントが存在しない"""
    pass


class ConflictError(CouchDBResponseError):
    """409: リビジョン競合など"""
    pass

