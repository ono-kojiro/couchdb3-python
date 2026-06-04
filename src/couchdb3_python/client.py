import httpx
from .urlresolver import URLResolver
from .exceptions import (
    HTTPError,
    CouchDBResponseError,
    NotFoundError,
    ConflictError,
)


class Client:
    """
    CouchDB への HTTP クライアント。
    URLResolver を使って URL を生成し、httpx で通信する。
    """

    #def __init__(self, base_url: str, *, timeout: float = 5.0):
    #    self.resolver = URLResolver(base_url)
    #    self.timeout = timeout
    #    self._client = httpx.Client(timeout=timeout)

    def __init__(self, base_url: str, *, username: str | None = None,
                 password: str | None = None, timeout: float = 5.0):

        self.resolver = URLResolver(base_url)
        self.timeout = timeout

        # 認証設定
        auth = None
        if username and password:
            auth = (username, password)

        self._client = httpx.Client(timeout=timeout, auth=auth)

    def url(self, path: str) -> str:
        return self.resolver.resolve(path)

    # ---------------------------
    # 基本 HTTP メソッド
    # ---------------------------

    def get(self, path: str):
        url = self.url(path)
        resp = self._client.get(url)
        return self._handle_response(resp, url)

    def put(self, path: str, json=None):
        url = self.url(path)
        resp = self._client.put(url, json=json)
        return self._handle_response(resp, url)

    def delete(self, path: str):
        url = self.url(path)
        resp = self._client.delete(url)
        return self._handle_response(resp, url)

    def head(self, path: str):
        url = self.url(path)
        resp = self._client.head(url)
        if resp.status_code == 404:
            raise NotFoundError("not_found", "Resource not found", status=404, url=url)
        if resp.is_error:
            raise HTTPError(resp.status_code, resp.text, url=url)
        return resp

    # ---------------------------
    # エラーハンドリング
    # ---------------------------

    def _handle_response(self, resp: httpx.Response, url: str):
        # HTTP レベルのエラー
        if resp.status_code >= 400:
            try:
                data = resp.json()
                if "error" in data and "reason" in data:
                    error = data["error"]
                    reason = data["reason"]

                    if resp.status_code == 404:
                        raise NotFoundError(error, reason, status=404, url=url)
                    if resp.status_code == 409:
                        raise ConflictError(error, reason, status=409, url=url)

                    raise CouchDBResponseError(error, reason, status=resp.status_code, url=url)
            except ValueError:
                # JSON でない場合
                raise HTTPError(resp.status_code, resp.text, url=url)

        # 正常系
        if resp.headers.get("content-type", "").startswith("application/json"):
            return resp.json()
        return resp.text

