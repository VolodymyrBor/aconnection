import abc
import asyncio
from typing import Self, override


class AsyncClosable(abc.ABC):

    @abc.abstractmethod
    async def close(self):
        pass

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


class AsyncConnectable(abc.ABC):

    @abc.abstractmethod
    async def connect(self):
        pass

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return None


class AsyncResourceManager(AsyncConnectable, AsyncClosable, abc.ABC):

    @override
    async def __aenter__(self) -> Self:
        await self.connect()
        return self

    @override
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


class AsyncConnectionManager[T](AsyncResourceManager, abc.ABC):

    def __init__(self):
        super().__init__()
        self._connection: T | None = None
        self._lock = asyncio.Lock()

    @override
    async def connect(self):
        async with self._lock:
            if self._connection is not None:
                raise ConnectionError('Connection is already created')
            self._connection = await self._create_connection()

    @override
    async def close(self):
        if self._connection is None:
            return
        async with self._lock:
            self._connection = None

    @property
    def _connected_conn(self) -> T:
        if self._connection is None:
            raise ConnectionError("Connection is not created")
        return self._connection

    @abc.abstractmethod
    async def _create_connection(self) -> T:
        pass
