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

    #def __init__(self, base_url: str, *, timeout: float = 5.0):
    #    self.resolver = URLResolver(base_url)
    #    self.timeout = timeout
    #    self._client = httpx.Client(timeout=timeout)

    def __init__(self, base_url: str, *, username: str | None = None,
                password: str | None = None, timeout: float = 5.0,
                verify: bool = True):

        self.resolver = URLResolver(base_url)
        self.timeout = timeout

        auth = None
        if username and password:
            auth = (username, password)

        self._client = httpx.Client(timeout=timeout, auth=auth, verify=verify)

    def url(self, path: str) -> str:
        return self.resolver.resolve(path)

    # ---------------------------
    # 基本 HTTP メソッド
    # ---------------------------

    def get(self, path: str, params=None, headers=None):
        url = self.url(path)
        resp = self._client.get(url, params=params, headers=headers)
        return self._handle_response(resp, url)

    def put(self, path: str, json=None, headers=None):
        url = self.url(path)
        resp = self._client.put(url, json=json, headers=headers)
        return self._handle_response(resp, url)

    def delete(self, path: str, headers=None):
        url = self.url(path)
        resp = self._client.delete(url, headers=headers)
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
        ctype = resp.headers.get("content-type", "")

        # エラー系
        if resp.status_code >= 400:
            # JSON 以外のエラーはそのまま HTTPError にする
            if not ctype.startswith("application/json"):
                raise HTTPError(resp.status_code, resp.text, url=url)

            # JSON エラー
            try:
                data = resp.json()
            except ValueError:
                raise HTTPError(resp.status_code, resp.text, url=url)

            # CouchDB 形式のエラー
            if "error" in data and "reason" in data:
                error = data["error"]
                reason = data["reason"]

                if resp.status_code == 404:
                    raise NotFoundError(error, reason, status=404, url=url)
                if resp.status_code == 409:
                    raise ConflictError(error, reason, status=409, url=url)

                raise CouchDBResponseError(error, reason, status=resp.status_code, url=url)

            # error/reason が無い → CouchDB エラーではない
            raise HTTPError(resp.status_code, resp.text, url=url)

        # 正常系
        if ctype.startswith("application/json"):
            return resp.json()

        # compact() のように JSON でないが {"ok": true} を期待されるケース
        if resp.status_code == 202:
            return {"ok": True}

        return resp.text

    def post(self, path: str, json=None, headers=None):
        url = self.url(path)

        # compact の場合は raw HTTP を送る
        if path.endswith("/_compact") and json is None:
            with httpcore.ConnectionPool() as pool:
                method = b"POST"
                hdrs = [] if headers is None else [(k.encode(), v.encode()) for k, v in headers.items()]
                content = b""
                _, _, resp = pool.request(method, url.encode(), hdrs, content)
                status, hdrs, body = resp
                response = httpx.Response(status, headers=dict(hdrs), content=body)
                return self._handle_response(response, url)

        # 通常の POST
        if json is None:
            resp = self._client.post(url, content=b"", headers=headers)
        else:
            resp = self._client.post(url, json=json, headers=headers)

        return self._handle_response(resp, url)
