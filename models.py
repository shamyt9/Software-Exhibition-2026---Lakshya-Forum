from flask_login import UserMixin
from database import users_col
from bson import ObjectId

class User(UserMixin):
    def __init__(self, user_data):
        self.id           = str(user_data["_id"])
        self.username     = user_data["username"]
        self.full_name    = user_data["full_name"]
        self.role         = user_data["role"]
        self.district     = user_data["district"]
        self._is_active   = user_data.get("is_active", True)  # store privately

    @property
    def is_active(self):
        return self._is_active

    @staticmethod
    def get_by_id(user_id):
        data = users_col.find_one({"_id": ObjectId(user_id)})
        return User(data) if data else None

    @staticmethod
    def get_by_username(username):
        data = users_col.find_one({"username": username})
        return User(data) if data else None

    def get_id(self):
        return self.id