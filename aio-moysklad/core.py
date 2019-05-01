class MetaData:
    __slots__ = [
        'href',
        'metadataHref',
        'type',
        'mediaType',
        'uuidHref',
        'size',
        'limit',
        'offset',
        'uuid',
    ]

    def __init__(self, meta: dict = None, *,
                 href=None, metadata_href=None, object_type=None, media_type=None, uuid_href=None, uuid=None,
                 limit=100, size=0, offset=0):
        """
        MetaData
        https://online.moysklad.ru/api/remap/1.1/doc/index.html#header-%D0%BC%D0%B5%D1%82%D0%B0%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D0%B5
        :param href:
        :param metadata_href:
        :param object_type: type in API
        :param media_type:
        :param uuid_href:
        """

        self.href = href
        self.metadataHref = metadata_href
        self.type = object_type
        self.mediaType = media_type
        self.uuidHref = uuid_href
        self.limit = limit
        self.offset = offset
        self.size = size
        self.uuid = uuid

        if meta:
            for field in self.__slots__:
                value = meta.get(field)
                if value is not None:
                    setattr(self, field, value)

        if self.uuidHref:
            _id = self.uuidHref.split('=')[-1] if '?id=' in self.uuidHref else None
            self.uuid = _id

    def data(self) -> dict:
        return {
            f: getattr(self, f) for f in self.__slots__
        }





