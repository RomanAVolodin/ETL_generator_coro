import json
from json import JSONDecodeError
from logging import Logger
from typing import Optional

from .base_storage import BaseStorage


class JsonFileStorage(BaseStorage):
    def __init__(
        self, logger: Logger, file_path: Optional[str] = 'storage.json'
    ):
        self.file_path = file_path
        self._logger = logger

    def save_state(self, state: dict) -> None:
        with open(self.file_path, 'w') as outfile:
            json.dump(state, outfile)

    def retrieve_state(self) -> dict:
        try:
            with open(self.file_path, 'r') as json_file:
                return json.load(json_file)
        except (FileNotFoundError, JSONDecodeError):
            self._logger.warning(
                'No state file provided. Continue with default file'
            )
            return dict()
