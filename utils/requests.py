from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Literal, Mapping

import httpx
from httpx import Headers, Response
from httpx._types import (
    CookieTypes,
    QueryParamTypes,
    RequestContent,
    RequestData,
    RequestFiles,
    TimeoutTypes,
    URLTypes,
    VerifyTypes,
)

from . import async_retry


default_proxy = None
"TODO 默认代理"

HeaderTypes = Headers | Mapping[str, str]


class Requests:
    """
    说明：

        异步访问模块

    """

    @classmethod
    def _get_proxy(cls, proxy: bool | str) -> str | None:
        if proxy is True:
            return default_proxy
        elif proxy is False:
            return None
        else:
            return proxy

    @classmethod
    @async_retry(max_tries=3)
    async def get(
        cls,
        url: str,
        *,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        allow_redirects: bool = True,
        timeout: TimeoutTypes = 30,
        proxy: bool | str = False,
        verify: bool = True,
        http2: bool = False,
        **kwargs,
    ) -> Response:
        """
        说明:

            发送Get请求

        参数:

            * ``url``: url
            * ``params``: 参数
            * ``headers``: 请求头
            * ``cookies``: cookies
            * ``allow_redirects``: 是否允许重定向
            * ``timeout``: 超时时间
            * ``proxy``: 是否使用代理，可输入自定义代理地址
            * ``verify``: 是否检查证书
            * ``http2``: 是否使用 HTTP/2
            * ``kwargs``: 传递给 `httpx.AsyncClient` 的其他参数

        """
        proxies = cls._get_proxy(proxy)
        async with httpx.AsyncClient(
            proxies=proxies, verify=verify, http2=http2, **kwargs
        ) as client:
            return await client.get(
                url,
                params=params,
                headers=headers,
                cookies=cookies,
                follow_redirects=allow_redirects,
                timeout=timeout,
            )

    @classmethod
    @async_retry(max_tries=3)
    async def post(
        cls,
        url: str,
        *,
        data: RequestData | None = None,
        content: RequestContent | None = None,
        files: RequestFiles | None = None,
        json: Any | None = None,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        allow_redirects: bool = True,
        timeout: TimeoutTypes = 30,
        proxy: bool | str = False,
        verify: bool = True,
        http2: bool = False,
        **kwargs,
    ) -> Response:
        """
        说明:

            发送Post请求

        参数:

            * ``url``: url
            * ``params``: 参数
            * ``data``: 数据
            * ``headers``: 请求头
            * ``cookies``: cookies
            * ``allow_redirects``: 是否允许重定向
            * ``timeout``: 超时时间
            * ``content``: content
            * ``files``: 文件
            * ``json``: json
            * ``proxy``: 是否使用代理，可输入自定义代理地址
            * ``verify``: 是否检查证书
            * ``http2``: 是否使用 HTTP/2
            * ``kwargs``: 传递给 `httpx.AsyncClient` 的其他参数

        """
        proxies = cls._get_proxy(proxy)
        async with httpx.AsyncClient(
            proxies=proxies, verify=verify, http2=http2, **kwargs
        ) as client:
            return await client.post(
                url,
                content=content,
                data=data,
                files=files,
                json=json,
                params=params,
                headers=headers,
                cookies=cookies,
                follow_redirects=allow_redirects,
                timeout=timeout,
            )

    @classmethod
    @async_retry(max_tries=3)
    async def put(
        cls,
        url: str,
        *,
        data: RequestData | None = None,
        content: RequestContent | None = None,
        files: RequestFiles | None = None,
        json: Any | None = None,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        allow_redirects: bool = True,
        timeout: TimeoutTypes = 30,
        proxy: bool | str = False,
        verify: bool = True,
        http2: bool = False,
        **kwargs,
    ) -> Response:
        """
        说明:

            发送 Put 请求

        参数:

            * ``url``: url
            * ``params``: 参数
            * ``data``: 数据
            * ``headers``: 请求头
            * ``cookies``: cookies
            * ``allow_redirects``: 是否允许重定向
            * ``timeout``: 超时时间
            * ``content``: content
            * ``files``: 文件
            * ``json``: json
            * ``proxy``: 是否使用代理，可输入自定义代理地址
            * ``verify``: 是否检查证书
            * ``http2``: 是否使用 HTTP/2
            * ``kwargs``: 传递给 `httpx.AsyncClient` 的其他参数

        """
        proxies = cls._get_proxy(proxy)
        async with httpx.AsyncClient(
            proxies=proxies, verify=verify, http2=http2, **kwargs
        ) as client:
            return await client.put(
                url,
                content=content,
                data=data,
                files=files,
                json=json,
                params=params,
                headers=headers,
                cookies=cookies,
                follow_redirects=allow_redirects,
                timeout=timeout,
            )

    @classmethod
    @async_retry(max_tries=3)
    async def patch(
        cls,
        url: str,
        *,
        data: RequestData | None = None,
        content: RequestContent | None = None,
        files: RequestFiles | None = None,
        json: Any | None = None,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        allow_redirects: bool = True,
        timeout: TimeoutTypes = 30,
        proxy: bool | str = False,
        verify: bool = True,
        http2: bool = False,
        **kwargs,
    ) -> Response:
        """
        说明:

            发送 Patch 请求

        参数:

            * ``url``: url
            * ``params``: 参数
            * ``data``: 数据
            * ``headers``: 请求头
            * ``cookies``: cookies
            * ``allow_redirects``: 是否允许重定向
            * ``timeout``: 超时时间
            * ``content``: content
            * ``files``: 文件
            * ``json``: json
            * ``proxy``: 是否使用代理，可输入自定义代理地址
            * ``verify``: 是否检查证书
            * ``http2``: 是否使用 HTTP/2
            * ``kwargs``: 传递给 `httpx.AsyncClient` 的其他参数

        """
        proxies = cls._get_proxy(proxy)
        async with httpx.AsyncClient(
            proxies=proxies, verify=verify, http2=http2, **kwargs
        ) as client:
            return await client.patch(
                url,
                content=content,
                data=data,
                files=files,
                json=json,
                params=params,
                headers=headers,
                cookies=cookies,
                follow_redirects=allow_redirects,
                timeout=timeout,
            )

    @classmethod
    async def delete(
        cls,
        url: URLTypes,
        *,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        allow_redirects: bool = True,
        timeout: TimeoutTypes | None = None,
        verify: VerifyTypes = True,
        http2: bool = False,
        proxy: str | bool = False,
        **kwargs,
    ) -> Response:
        """
        说明:

            发起 Delete 请求。

        参数:

            * ``url``: 请求地址
            * ``params``: 请求参数
            * ``headers``: 请求头
            * ``cookies``: 请求 Cookie
            * ``follow_redirects``: 是否跟随重定向
            * ``timeout``: 超时时间，单位: 秒
            * ``verify``: 是否验证 SSL 证书
            * ``http2``: 是否使用 HTTP/2
            * ``proxy``: 代理地址
            * ``kwargs``: 传递给 `httpx.AsyncClient` 的其他参数

        """
        proxies = cls._get_proxy(proxy)
        async with httpx.AsyncClient(
            verify=verify, http2=http2, proxies=proxies, **kwargs
        ) as client:
            return await client.delete(
                url,
                params=params,
                headers=headers,
                cookies=cookies,
                follow_redirects=allow_redirects,
                timeout=timeout,
            )

    @classmethod
    @async_retry(max_tries=3)
    async def head(
        cls,
        url: str,
        *,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        allow_redirects: bool = True,
        timeout: TimeoutTypes = 30,
        proxy: bool | str = False,
        verify: bool = True,
        http2: bool = False,
        **kwargs,
    ) -> Response:
        """
        说明:

            发送head请求

        参数:

            * ``url``: url
            * ``params``: 参数
            * ``headers``: 请求头
            * ``cookies``: cookies
            * ``allow_redirects``: 是否允许重定向
            * ``timeout``: 超时时间
            * ``proxy``: 是否使用代理，可输入自定义代理地址
            * ``verify``: 是否检查证书
            * ``http2``: 是否使用 HTTP/2
            * ``kwargs``: 传递给 `httpx.AsyncClient` 的其他参数

        """
        proxies = cls._get_proxy(proxy)
        async with httpx.AsyncClient(
            proxies=proxies, verify=verify, http2=http2, **kwargs
        ) as client:
            return await client.head(
                url,
                params=params,
                headers=headers,
                cookies=cookies,
                follow_redirects=allow_redirects,
                timeout=timeout,
            )

    @classmethod
    @async_retry(max_tries=3)
    async def options(
        cls,
        url: str,
        *,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        allow_redirects: bool = True,
        timeout: TimeoutTypes = 30,
        proxy: bool | str = False,
        verify: bool = True,
        http2: bool = False,
        **kwargs,
    ) -> Response:
        """
        说明:

            发送 Options 请求

        参数:

            * ``url``: url
            * ``params``: 参数
            * ``headers``: 请求头
            * ``cookies``: cookies
            * ``allow_redirects``: 是否允许重定向
            * ``timeout``: 超时时间
            * ``proxy``: 是否使用代理，可输入自定义代理地址
            * ``verify``: 是否检查证书
            * ``http2``: 是否使用 HTTP/2
            * ``kwargs``: 传递给 `httpx.AsyncClient` 的其他参数

        """
        proxies = cls._get_proxy(proxy)
        async with httpx.AsyncClient(
            proxies=proxies, verify=verify, http2=http2, **kwargs
        ) as client:
            return await client.options(
                url,
                params=params,
                headers=headers,
                cookies=cookies,
                follow_redirects=allow_redirects,
                timeout=timeout,
            )


    @classmethod
    @asynccontextmanager
    async def stream(
        cls,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"],
        url: URLTypes,
        *,
        content: RequestContent | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
        json: Any = None,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        allow_redirects: bool = True,
        timeout: TimeoutTypes | None = None,
        verify: VerifyTypes = True,
        http2: bool = False,
        proxy: bool | str = False,
        **kwargs,
    ) -> AsyncGenerator[Response, None]:
        """
        说明:

            发起流式请求。

        参数:

            * ``method``: 请求方法
            * ``url``: 请求地址
            * ``content``: 请求内容
            * ``data``: 请求数据
            * ``files``: 请求文件
            * ``json``: 请求 JSON
            * ``params``: 请求参数
            * ``headers``: 请求头
            * ``cookies``: 请求 Cookie
            * ``allow_redirects``: 是否跟随重定向
            * ``timeout``: 超时时间，单位: 秒
            * ``verify``: 是否验证 SSL 证书
            * ``http2``: 是否使用 HTTP/2
            * ``proxy``: 代理地址
            * ``kwargs``: 传递给 `httpx.AsyncClient` 的其他参数

        """
        proxies = cls._get_proxy(proxy)
        async with httpx.AsyncClient(
            verify=verify, http2=http2, proxies=proxies, **kwargs
        ) as client, client.stream(
            method,
            url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            follow_redirects=allow_redirects,
            timeout=timeout,
        ) as response:
            yield response

    @classmethod
    @asynccontextmanager
    async def client_session(
        cls,
        verify: VerifyTypes = True,
        http2: bool = False,
        proxy: str | bool = False,
        allow_redirects: bool = True,
        **kwargs,
    ) -> AsyncGenerator[httpx.AsyncClient, None]:
        """
        说明:

            创建 `httpx.AsyncClient` 会话。

        参数:

            * ``verify``: 是否验证 SSL 证书
            * ``http2``: 是否使用 HTTP/2
            * ``proxy``: 地址
            * ``allow_redirects``: 是否跟随重定向
            * ``kwargs``: 传递给 `httpx.AsyncClient` 的其他参数

        """
        proxies = cls._get_proxy(proxy)
        async with httpx.AsyncClient(
            verify=verify,
            http2=http2,
            proxies=proxies,
            follow_redirects=allow_redirects,
            **kwargs,
        ) as client:
            yield client


from html import escape as escape
from html import unescape as unescape
from urllib.parse import quote as quote
from urllib.parse import unquote as unquote

from httpx import Cookies as Cookies
from httpx import HTTPError as HTTPError
from httpx import HTTPStatusError as HTTPStatusError
from httpx import ReadError as ReadError
