from pydantic import BaseModel, Field, EmailStr


class UserSchema(BaseModel):
    id: int = Field(default=None)
    name: str = Field(...)
    username: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "id": 7,
                "name": "Jessica Grady",
                "username": "Merle.Hammes",
                "email": "fidel-rodrigues65@hotmail.com",
                "password": "12345678"
            }
        }

class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "fidel-rodrigues65@hotmail.com",
                "password": "12345678"
            }
        }