import result


class TestException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


error = result.Err("error")

result = error.unwrap_or_raise(TestException)
