import asyncio
from typing import override
from unittest import mock

import pytest

from connectable import AsyncClosable, AsyncConnectable, AsyncConnectionManager, AsyncResourceManager


class TestAsyncClosable:

    class _Closable(AsyncClosable):

        def __init__(self):
            self.on_close = mock.AsyncMock()

        @override
        async def close(self):
            await self.on_close()

    async def test_close(self):
        closable = self._Closable()
        await closable.close()
        closable.on_close.assert_called_once()

    async def test_context(self):
        async with self._Closable() as closable:
            closable.on_close.assert_not_called()
        closable.on_close.assert_called_once()


class TestAsyncConnectable:

    class _Connectable(AsyncConnectable):

        def __init__(self):
            self.on_connect = mock.AsyncMock()

        @override
        async def connect(self):
            await self.on_connect()

    async def test_connect(self):
        connectable = self._Connectable()
        await connectable.connect()
        connectable.on_connect.assert_called_once()

    async def test_context(self):
        async with self._Connectable() as connectable:
            connectable.on_connect.assert_called_once()


class TestAsyncResourceManager:

    class _ResourceManager(AsyncResourceManager):
        def __init__(self):
            self.on_connect = mock.AsyncMock()
            self.on_close = mock.AsyncMock()

        @override
        async def connect(self):
            await self.on_connect()

        @override
        async def close(self):
            await self.on_close()

    async def test_connect(self):
        resource_manager = self._ResourceManager()
        await resource_manager.connect()
        resource_manager.on_connect.assert_called_once()

    async def test_close(self):
        resource_manager = self._ResourceManager()
        await resource_manager.close()
        resource_manager.on_close.assert_called_once()

    async def test_context(self):
        async with self._ResourceManager() as resource_manager:
            resource_manager.on_connect.assert_called_once()
        resource_manager.on_close.assert_called_once()


class TestAsyncConnectionManager:

    class _ConnectionManager(AsyncConnectionManager[int]):

        @override
        async def _create_connection(self) -> int:
            return 1

    async def test_connect_close(self):
        connection_manager = self._ConnectionManager()
        assert connection_manager._connection is None
        await connection_manager.connect()
        assert connection_manager._connected_conn == 1
        await connection_manager.close()
        assert connection_manager._connection is None

    async def test_context(self):
        async with self._ConnectionManager() as connection_manager:
            assert connection_manager._connected_conn == 1
            assert connection_manager.connected
        assert connection_manager._connection is None

    def test_access_to_not_created_connection(self):
        connection_manager = self._ConnectionManager()
        with pytest.raises(ConnectionError):
            _ = connection_manager._connected_conn

    async def test_multiple_connect(self):
        connection_manager = self._ConnectionManager()
        await connection_manager.connect()
        with pytest.raises(ConnectionError):
            await connection_manager.connect()

    async def test_multiple_connect_parallel(self):
        connection_manager = self._ConnectionManager()
        tasks = [
            connection_manager.connect()
            for _ in range(3)
        ]
        with pytest.raises(ConnectionError):
            await asyncio.gather(*tasks)

    async def test_multiple_close_parallel(self):
        connection_manager = self._ConnectionManager()
        await connection_manager.connect()
        tasks = [
            connection_manager.close()
            for _ in range(3)
        ]
        await asyncio.gather(*tasks)
