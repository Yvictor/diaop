class AuthenticationService:

    def __init__(self) -> None:
        pass

    def verify(self, account: str, password: str, otp: str) -> bool:
        raise NotImplementedError()
