from dataclasses import dataclass
import http


@dataclass()
class Response[T]:
    status: http.HTTPStatus
    data: T | None
    message: str
