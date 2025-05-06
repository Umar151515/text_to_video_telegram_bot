from config.manager import ConfigManager


class User:
    def __init__(self, id: int):
        from .messages import Messages
        self.id = id
        self.number_requests = 5
        self.full_access = False