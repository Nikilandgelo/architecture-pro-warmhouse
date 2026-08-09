from pydantic import BaseModel


class SuccessfulResponse(BaseModel):
    success: bool = True
