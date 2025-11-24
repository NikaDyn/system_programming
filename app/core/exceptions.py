# ===========================
# Кастомні виключення для API
# ===========================

class CategoryNotFound(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class CategoryAlreadyExists(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class PlaceNotFound(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class FavoriteAlreadyExists(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class FavoriteNotFound(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class UserAlreadyExists(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class UserNotFound(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class CredentialsException(Exception):
    def __init__(self, title: str, detail: str):
        self.title = title
        self.detail = detail
        super().__init__(f"{title}: {detail}")


class InactiveUser(Exception):
    def __init__(self, title: str, detail: str):
        self.title = title
        self.detail = detail
        super().__init__(f"{title}: {detail}")


class PermissionDenied(Exception):
    def __init__(self, title: str, detail: str):
        self.title = title
        self.detail = detail
        super().__init__(f"{title}: {detail}")
