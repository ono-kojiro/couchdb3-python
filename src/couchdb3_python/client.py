import httpx
import httpcore
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

    def __init__(
        self,
        base_url: str,
        *,
        username: str | None = None,
        password: str | None = None,
        timeout: float = 5.0,
        verify: bool = True,
    ):
        self.resolver = URLResolver(base_url)
        self.timeout = timeout

        # 認証設定
        auth = None
        if username and password:
            auth = (username, password)

        # verify を外部から指定できるようにした
        self._client = httpx.Client(timeout=timeout, auth=auth, verify=verify)

    def url(self, path: str) -> str:
        return self.resolver.resolve(path)

    # ---------------------------
    # request() — すべての HTTP メソッドの共通処理
    # ---------------------------
    def request(self, method: str, path: str, **kwargs):
        url = self.url(path)
        resp = self._client.request(method, url, **kwargs)
        return self._handle_response(resp, url)

    # ---------------------------
    # 基本 HTTP メソッド（request() に統一）
    # ---------------------------
    def get(self, path: str, **kwargs):
        return self.request("GET", path, **kwargs)

    def put(self, path: str, **kwargs):
        return self.request("PUT", path, **kwargs)

    def delete(self, path: str, **kwargs):
        return self.request("DELETE", path, **kwargs)

    def head(self, path: str, **kwargs):
        url = self.url(path)
        resp = self._client.head(url, **kwargs)
        if resp.status_code == 404:
            raise NotFoundError("not_found", "Resource not found", status=404, url=url)
        if resp.is_error:
            raise HTTPError(resp.status_code, resp.text, url=url)
        return resp

    def post(self, path: str, json=None, headers=None):
        return self.request("POST", path, json=json, headers=headers)

    # ---------------------------
    # エラーハンドリング
    # ---------------------------
    def _handle_response(self, resp: httpx.Response, url: str):
        ctype = resp.headers.get("content-type", "")

        # エラー系
        if resp.status_code >= 400:
            if not ctype.startswith("application/json"):
                raise HTTPError(resp.status_code, resp.text, url=url)

            try:
                data = resp.json()
            except ValueError:
                raise HTTPError(resp.status_code, resp.text, url=url)

            if "error" in data and "reason" in data:
                error = data["error"]
                reason = data["reason"]

                if resp.status_code == 404:
                    raise NotFoundError(error, reason, status=404, url=url)
                if resp.status_code == 409:
                    raise ConflictError(error, reason, status=409, url=url)

                raise CouchDBResponseError(error, reason, status=resp.status_code, url=url)

            raise HTTPError(resp.status_code, resp.text, url=url)

        # 正常系
        if ctype.startswith("application/json"):
            return resp.json()

        if resp.status_code == 202:
            return {"ok": True}

        return resp.text
