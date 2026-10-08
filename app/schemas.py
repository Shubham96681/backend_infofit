from pydantic import BaseModel, ConfigDict

class TicketCreate(BaseModel):
    title: str
    details: str

class TicketUpdate(BaseModel):
    title: str
    details: str
    status: str

class TicketResponse(BaseModel):
    id: int
    title: str
    details: str
    status: str

    model_config = ConfigDict(from_attributes=True)