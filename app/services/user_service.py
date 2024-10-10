from django.contrib.auth import authenticate
from app.models import CustomUser


class UserService:

    @staticmethod
    def get_user(*args, **kwargs):
        try:
            return CustomUser.objects.get(*args, **kwargs)
        except CustomUser.DoesNotExist as e:
            return None

    @staticmethod
    def filter_user(*args, **kwargs):
        return CustomUser.objects.filter(*args, **kwargs)

    @classmethod
    def login_user(cls, email, password):
        if email == "" or password == "":
            return False, "Fields cannot be empty", None
        user = authenticate(email=email, password=password)
        if not user:
            return False, "Email or password didn't matched", None
        return True, "Successfully logged in", user

    @classmethod
    def register_user(cls, email, password, confirm_password, role):
        if email == "" or password == "" or confirm_password == "" or role == "":
            return False, "Fields cannot be empty", None
        user = cls.get_user(email=email)
        if user:
            return False, "Email already exists", None
        if password != confirm_password:
            return False, "Password didn't matched", None
        valid_roles = [CustomUser.AUCTIONEER, CustomUser.BIDDER]
        if role not in valid_roles:
            return False, "Invalid Role", None
        user = CustomUser.objects.create_user(email=email, password=password, role=role)
        return True, "Successfully registered", user
