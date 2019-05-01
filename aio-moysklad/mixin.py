from .utils import TaskQueue


def wait_free_slot(func):
    """
    decorator for request function
    1) try get slot from rpp queue or wait new free slot
    2) if get slot from rpr, try get slot from parallel queue or wait free slot
    :param func:
    :return:
    """

    async def wrapper(self, *args, **kwargs):
        await self._queue_rpp.get()  # try get rpp slot
        await self._queue_parallel.get()  # try get parallel slot
        response = await func(self, *args, **kwargs)
        self._queue_parallel.put_nowait(1)  # free parallel slot
        return response

    return wrapper


class LimitRateDriverMixin:
    """
    Control request rate
    """
    REQUEST_PER_PERIOD = 100  # not more 100 request per period
    REQUEST_PERIOD = 5

    PRS = 20  # request per second
    MAX_PARALLEL_REQUEST_COUNT = 5  # not more 5 parallel requests for user

    def __init__(self,
                 request_per_preiod: int = None,
                 requests_period: int = None,
                 max_parallel_request_count: int = None,
                 *args, **kwargs
                 ):
        """
        _queue_parallel - control max parallel request
        _queue_rps - control request per period
        :param request_per_preiod:
        :param requests_period:
        :param max_parallel_request_count:
        """
        super().__init__(*args, **kwargs)
        self._queue_parallel = TaskQueue(
            max_parallel_request_count or LimitRateDriverMixin.MAX_PARALLEL_REQUEST_COUNT
        )

        self._queue_rpp = TaskQueue(
            request_per_preiod or LimitRateDriverMixin.REQUEST_PER_PERIOD,
            requests_period or LimitRateDriverMixin.REQUEST_PERIOD
        )

    @wait_free_slot
    async def get(self, *args, **kwargs):
        return await super().get(*args, **kwargs)

    @wait_free_slot
    async def post(self, *args, **kwargs):
        return await super().post(*args, **kwargs)

    @wait_free_slot
    async def put(self, *args, **kwargs):
        return await super().put(*args, **kwargs)

    @wait_free_slot
    async def delete(self, *args, **kwargs):
        return await super().delete(*args, **kwargs)

    async def close(self):
        await super().close()
        self._queue_parallel.canel()
        self._queue_rpp.canel()
