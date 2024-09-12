from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData[T: str | None](BaseModel):
    username: T = None

    @property
    def email(self) -> T:
        """Alias for username"""
        return self.username
