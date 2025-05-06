from pathlib import Path
import pickle

from ..models.user import User
from config import user_data_path


class UserLogic:
    _users: dict[int, User] = {}

    @classmethod
    def load(cls) -> None:
        try:
            with open(user_data_path, "rb") as file:
                cls._users = pickle.load(file)
        except (FileNotFoundError, EOFError):
            cls._users = {}

    @classmethod
    def save(cls) -> None:
        Path("data").mkdir(exist_ok=True)
        with open(user_data_path, "wb") as file:
            pickle.dump(cls._users, file)

    @classmethod
    def get_user(cls, user_id: int, auto_creation:bool = True) -> User | None:
        user = cls._users.get(user_id)
        if auto_creation and not user:
            user = User(user_id)
            cls.set_user(user)
        return user

    @classmethod
    def set_user(cls, user: User) -> None:
        cls._users[user.id] = user
        cls.save()

    @classmethod
    def delete_user(cls, user_id: int) -> bool:
        if user_id in cls._users:
            del cls._users[user_id]
            cls.save()
            return True
        return False