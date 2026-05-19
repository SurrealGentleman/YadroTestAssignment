from pydantic import BaseModel, ConfigDict


class PersonRead(BaseModel):
    id: int
    gender: str
    first_name: str
    last_name: str
    phone: str
    email: str
    address: str

    model_config = ConfigDict(from_attributes=True)

