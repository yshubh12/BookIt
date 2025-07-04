from fastapi import FastAPI
from pydantic import BaseModel
from calendar_utils import get_available_slots, book_slot
from agent import handle_user_input
from calendar_utils import get_upcoming_appointments

app = FastAPI()

class UserInput(BaseModel):
    message: str

class SlotInput(BaseModel):
    slot: str

@app.post("/chat")
def chat(input: UserInput):
    response = handle_user_input(input.message)
    return {"response": response}

@app.get("/slots")
def get_slots():
    slots = get_available_slots()
    return {"slots": slots}

@app.post("/book")
def confirm_booking(data: SlotInput):
    success = book_slot(data.slot)
    if success:
        return {"status": "success"}
    else:
        return {"status": "failed"}


@app.get("/appointments")
def view_appointments():
    upcoming = get_upcoming_appointments()
    return {"appointments": upcoming}
