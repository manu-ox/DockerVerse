from pyrogram.types import InlineKeyboardButton
from typing import Callable
from abc import ABC, abstractmethod
import re



class CommandHandler(ABC):
    raw_handler: Callable
    pattern: re.Pattern

    def __init__(self):
        self.pattern = re.compile(rf'^/({self._command})$', re.IGNORECASE)

    def set_handler(self, handler: Callable):
        self.raw_handler = handler
        return handler

    @property
    @abstractmethod
    def _command(self) -> str:
        ...


class ButtonHandler(ABC):
    raw_handler: Callable
    pattern: re.Pattern

    def __init__(self):
        self.pattern = re.compile(self._data_format)

    def set_handler(self, handler: Callable):
        self.raw_handler = handler
        return handler
    
    @property
    @abstractmethod
    def _data_format(self) -> str:
        ...
    
    def button(self, button_text: str, /):
        return InlineKeyboardButton(
            text=button_text,
            callback_data=self._data_format
        )


class ContainerControlButtonHandler(ButtonHandler):
    _data_format = 'CONTAINER-{method}-{container_id}'
    _container_id_pattern = r'[a-f0-9]{12}'

    def __init__(self):
        pattern = self._data_format.format(
            method=self._method,
            container_id=self._container_id_pattern
        )

        self.pattern = re.compile(pattern)

    @property
    @abstractmethod
    def _method(self) -> str:
        ...

    def button(self, button_text: str, /, *, container_id: str):
        return InlineKeyboardButton(
            text=button_text,
            callback_data=self._data_format.format(method=self._method, container_id=container_id)
        )
    
    @staticmethod
    def get_container_id(data: str):
        return data.split('-', 2)[2]


class LogsButtonHandler(ButtonHandler):
    _data_format = 'LOGS-{method}-{container_id}-{number}'
    _container_id_pattern = r'[a-f0-9]{12}'
    _number_pattern = r'\d+'

    def __init__(self):
        pattern = self._data_format.format(
            method=self._method,
            container_id=self._container_id_pattern,
            number=self._number_pattern,
        )

        self.pattern = re.compile(pattern)
    
    @property
    @abstractmethod
    def _method(self) -> str:
        ...

    def button(self, button_text: str, /, *, container_id: str, number: int):
        return InlineKeyboardButton(
            text=button_text,
            callback_data=self._data_format.format(
                method=self._method,
                container_id=container_id,
                number=number,
            )
        )
    
    def get_container_id(self, data: str):
        return data.split('-', 3)[2]
    
    def get_number(self, data: str):
        return int(data.split('-', 3)[3])
    
    