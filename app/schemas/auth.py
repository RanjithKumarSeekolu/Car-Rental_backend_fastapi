from pydantic import BaseModel

class TokenUser(BaseModel):
  uid: str
  email: str | None = None
  name: str | None = None