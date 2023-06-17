import abc


class BaseStorage:
    @abc.abstractmethod
    def save_state(self, state: dict) -> None:
        ...

    @abc.abstractmethod
    def retrieve_state(self) -> dict:
        ...
