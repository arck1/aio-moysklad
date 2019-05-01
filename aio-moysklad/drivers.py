import aiohttp
from .mixin import LimitRateDriverMixin


class BaseDriver:
    def __init__(self, timeout=10, loop=None):
        self.timeout = timeout
        self._loop = loop

    async def get(self, url, params, timeout=None):
        '''
        :param url:
        :param params: dict of query params
        :return: response
        '''
        raise NotImplementedError

    async def post(self, url, data, timeout=None):
        '''
        :param url:
        :param data: dict of payload
        :return: response
        '''
        raise NotImplementedError

    async def put(self, url, params, timeout=None):
        '''
        :param params: dict of query params
        :return: response
        '''
        raise NotImplementedError

    async def delete(self, url, data, timeout=None):
        '''
        :param data: dict pr string
        :return: response
        '''
        raise NotImplementedError

    async def close(self):
        raise NotImplementedError


class HttpDriver(BaseDriver):
    def __init__(self, timeout=10, loop=None, session=None, auth=None, json_serialize=None):
        super().__init__(timeout, loop)
        if not session:
            self.session = aiohttp.ClientSession(loop=loop, auth=auth, json_serialize=json_serialize)
        else:
            self.session = session

    async def get(self, url, params, timeout=None):
        async with self.session.get(url, params=params, timeout=timeout or self.timeout) as response:
            return response.status, await response.json()

    async def post(self, url, payload, timeout=None):  # TODO check payload
        async with self.session.post(url, json=payload, timeout=timeout or self.timeout) as response:
            return response.status, await response.json()

    async def put(self, url, data, timeout=None):  # TODO check data
        async with self.session.get(url, data=data, timeout=timeout or self.timeout) as response:
            return response.status, await response.json()

    async def delete(self, url, params, timeout=None):
        async with self.session.get(url, timeout=timeout or self.timeout) as response:
            return response.status, await response.json()

    async def close(self):
        await self.session.close()


class LimitedHttpDriver(LimitRateDriverMixin, HttpDriver):
    pass

