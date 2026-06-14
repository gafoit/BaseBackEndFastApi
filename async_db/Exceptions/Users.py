class LoginAlreadyExists(Exception):
    def __init__(self, login: str):
        self.login = login
        super().__init__(f"Login: {login} already taken")


class EmailAlreadyExists(Exception):
    def __init__(self, email: str):
        self.login = email
        super().__init__(f"Email: {email} already registered")


class UserDoesNotExist(Exception):
    def __init__(self):
        super().__init__(f"User does not exist")


class LoginDoesNotExist(Exception):
    def __init__(self, login: str):
        self.login = login
        super().__init__(f"User: {login} does not exist")


class UserBlocked(Exception):
    def __init__(self):
        super().__init__('User blocked')


class InvalidPassword(Exception):
    def __init__(self):
        super().__init__("Incorrect Password!")


class UserLoggedOut(Exception):
    def __init__(self):
        super().__init__('User logged out')


class UsernameAlreadyExists(Exception):
    def __init__(self, username: str):
        self.username = username
        super().__init__(f"Username: {username} already taken")


class RepeatsOldPassword(Exception):
    def __init__(self):
        super().__init__('The new password is no different from the old one')


class UnmatchedPassword(Exception):
    def __init__(self):
        super().__init__("The passwords don't match")
