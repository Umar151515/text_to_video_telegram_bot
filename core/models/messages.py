from __future__ import annotations

import os

from config import ConfigManager
from ..logic.user_logic import UserLogic

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .image import Image


class Messages:
    def __init__(self, messages:list[dict[str, str]]|"Messages"|None = None):
        if isinstance(messages, Messages):
            self.messages = messages.messages
        elif isinstance(messages, list):
            self.messages = messages
        else:
            self.messages = []
        self.images: list[Image] = []

    def add_message(self, role: str, content: str) -> None:
        self.messages.append({"role": role, "content": content})
        UserLogic.save()

    def add_image(self, role: str, image: Image) -> None:
        self.messages.append({"role": role, "content": str(image)})
        self.images.append(image)
        UserLogic.save()

    def get_messages(self) -> "Messages":
        return Messages([message for message in self.messages if message["role"] != "system"])
    
    def clear_messages(self):
        for image in self.images:
            if os.path.exists(image.file_path):
                os.remove(image.file_path)
        self.images.clear()
        self.messages.clear()

        UserLogic.save()