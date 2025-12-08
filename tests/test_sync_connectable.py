from typing import override
from unittest import mock

import pytest

from connectable import Closable, Connectable, ConnectionManager, ResourceManager


class TestClosable:

    class _Closable(Closable):

        def __init__(self):
            self.on_close = mock.MagicMock()

        @override
        def close(self):
            self.on_close()

    def test_close(self):
        closable = self._Closable()
        closable.close()
        closable.on_close.assert_called_once()

    def test_context(self):
        with self._Closable() as closable:
            closable.on_close.assert_not_called()
        closable.on_close.assert_called_once()


class TestConnectable:

    class _Connectable(Connectable):

        def __init__(self):
            self.on_connect = mock.MagicMock()

        @override
        def connect(self):
            self.on_connect()

    def test_connect(self):
        connectable = self._Connectable()
        connectable.connect()
        connectable.on_connect.assert_called_once()

    def test_context(self):
        with self._Connectable() as connectable:
            connectable.on_connect.assert_called_once()


class TestResourceManager:

    class _ResourceManager(ResourceManager):
        def __init__(self):
            self.on_connect = mock.MagicMock()
            self.on_close = mock.MagicMock()

        @override
        def connect(self):
            self.on_connect()

        @override
        def close(self):
            self.on_close()

    def test_connect(self):
        resource_manager = self._ResourceManager()
        resource_manager.connect()
        resource_manager.on_connect.assert_called_once()

    def test_close(self):
        resource_manager = self._ResourceManager()
        resource_manager.close()
        resource_manager.on_close.assert_called_once()

    def test_context(self):
        with self._ResourceManager() as resource_manager:
            resource_manager.on_connect.assert_called_once()
        resource_manager.on_close.assert_called_once()


class TestConnectionManager:

    class _ConnectionManager(ConnectionManager[int]):

        @override
        def _create_connection(self) -> int:
            return 1

    def test_connect_close(self):
        connection_manager = self._ConnectionManager()
        assert connection_manager._connection is None
        connection_manager.connect()
        assert connection_manager._connected_conn == 1
        connection_manager.close()
        assert connection_manager._connection is None

    def test_context(self):
        with self._ConnectionManager() as connection_manager:
            assert connection_manager._connected_conn == 1
        # pyrefly: ignore [unnecessary-comparison]
        assert connection_manager._connection is None

    def test_access_to_not_created_connection(self):
        connection_manager = self._ConnectionManager()
        with pytest.raises(ConnectionError):
            _ = connection_manager._connected_conn

    def test_multiple_connect(self):
        connection_manager = self._ConnectionManager()
        connection_manager.connect()
        with pytest.raises(ConnectionError):
            connection_manager.connect()
