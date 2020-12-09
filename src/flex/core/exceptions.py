class EntityNotFoundException(Exception):
    pass


class PasswordNotCorrectException(Exception):
    pass


class NotAuthorizedException(Exception):
    pass


class ProfileException(Exception):
    pass


class ProfileNotFoundException(ProfileException):
    pass
