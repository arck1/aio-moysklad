from .session import MSSession


class MSApi:

    def __init__(self, session: MSSession):
        self._session = session

    def __getattr__(self, method_name):
        return Request(self, method_name)

    async def __call__(self, method_name, **method_kwargs):
        return await getattr(self, method_name)(**method_kwargs)


class Request:
    __slots__ = (
        '_api',
        '_method_name',
        '_method_args',
    )

    def __init__(self, api, method_name):
        self._api = api
        self._method_name = method_name

    def __getattr__(self, method_name):
        return Request(self._api, f"{self._method_name}/{method_name}")

    async def __call__(self, **method_args):
        timeout = method_args.pop('timeout', None)
        method = method_args.pop('method', None)
        self._method_args = method_args

        return await self._api._session.send_request(
            method_name=self._method_name,
            method_args=method_args,
            timeout=timeout,
            method=method
        )
