from fastapi import HTTPException


class InvalidToken(Exception):
    pass

class AccessTokenRequired(Exception):
    pass

class RefreshTokenRequired(Exception):
    pass

class InsufficientPermission(Exception):
    pass

class UserAlreadyExists(Exception):
    pass