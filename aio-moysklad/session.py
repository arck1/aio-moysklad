import asyncio

import ujson
from aiohttp import BasicAuth

from .drivers import LimitedHttpDriver


class MSSession:
    API_URL = 'https://online.moysklad.ru/api'
    API_TYPE = 'remap'
    API_VERSION = '1.1'

    HTTP_METHODS = ['get', 'post', 'put', 'delete']

    def __init__(self, *, username, password, timeout=10, loop=None,
                 api_type=API_TYPE, api_version=API_VERSION, driver=None, json_serialize=ujson.dumps):
        self.username = username
        self.password = password
        self.timeout = timeout

        self.api_type = api_type
        self.api_verision = api_version

        self.request_url = f"{MSSession.API_URL}/{api_type}/{api_version}"

        self.basic_auth = self.get_auth_credentials()

        if loop is None:
            loop = asyncio.get_event_loop()

        self.driver = LimitedHttpDriver(
            timeout=timeout, auth=self.basic_auth, json_serialize=json_serialize, loop=loop
        ) if driver is None else driver

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return await self.driver.close()

    def get_auth_credentials(self):
        return BasicAuth(self.username, self.password)

    async def send_request(self, method_name, method_args, timeout=None, method=None):
        if method is None or (str(method).lower().strip() not in self.HTTP_METHODS):
            method = 'get'
        method = str(method).lower().strip()
        handler = getattr(self.driver, method, self.driver.get)

        response = await handler(f"{self.request_url}/{method_name}/", method_args, timeout=timeout)

        return response


