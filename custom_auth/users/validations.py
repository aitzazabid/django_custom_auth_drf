from users.models import User
import re


class Validation:

    @staticmethod
    def validate_email(email):
        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            return False
        return True

    @staticmethod
    def email_exists(email):
        if User.objects.filter(email=email).exists():
            return True
        return False

    @staticmethod
    def validate_password(password):
        if re.match(r"^(?=.*?[A-Z])(?=.*?[0-9]).{8,}$",password):
            return True
        return False