import abc
from typing import Self, override


class Closable(abc.ABC):

    @abc.abstractmethod
    def close(self):
        pass

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class Connectable(abc.ABC):

    @abc.abstractmethod
    def connect(self):
        pass

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return None


class ResourceManager(Connectable, Closable, abc.ABC):

    @override
    def __enter__(self) -> Self:
        self.connect()
        return self

    @override
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class ConnectionManager[T](ResourceManager, abc.ABC):

    def __init__(self):
        super().__init__()
        self._connection: T | None = None

    @property
    def connected(self) -> bool:
        return self._connection is not None

    @override
    def connect(self):
        if self._connection is not None:
            raise ConnectionError('Connection is already created')
        self._connection = self._create_connection()

    @override
    def close(self):
        self._connection = None

    @property
    def _connected_conn(self) -> T:
        if self._connection is None:
            raise ConnectionError("Connection is not created")
        return self._connection

    @abc.abstractmethod
    def _create_connection(self) -> T:
        pass
