
class AppError(Exception):
    status_code = 500
    default_message = "An application error occurred."

    def __init__(self, message: str | None = None):
        self.message = message or self.default_message
        super().__init__(self.message)


class NotFoundError(AppError):
    status_code = 404
    default_message = "Resource not found."


class ConflictError(AppError):
    status_code = 409
    default_message = "Resource already exists."


class UnauthorizedError(AppError):
    status_code = 401
    default_message = "Authentication required."


class ForbiddenError(AppError):
    status_code = 403
    default_message = "You do not have permission to perform this action."
