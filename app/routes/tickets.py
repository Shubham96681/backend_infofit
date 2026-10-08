from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Ticket
from ..schemas import TicketCreate, TicketResponse, TicketUpdate


router = APIRouter(
    prefix="/tickets",
    tags=["tickets"]
)


@router.get("/", response_model=list[TicketResponse])
def list_tickets(db: Session = Depends(get_db)):
    return db.query(Ticket).order_by(Ticket.id.desc()).all()


@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(
    ticket_id: int,
    db: Session = Depends(get_db)
):
    ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id
    ).first()

    if not ticket:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    return ticket


@router.post("/", response_model=TicketResponse)
def create_ticket(
    body: TicketCreate,
    db: Session = Depends(get_db)
):
    ticket = Ticket(
        title=body.title,
        details=body.details,
        status="Open"
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return ticket


@router.put("/{ticket_id}", response_model=TicketResponse)
def update_ticket(
    ticket_id: int,
    body: TicketUpdate,
    db: Session = Depends(get_db)
):
    ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id
    ).first()

    if not ticket:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    if body.status not in ("Open", "Done"):
        raise HTTPException(
            status_code=400,
            detail="Status must be Open or Done"
        )

    ticket.title = body.title
    ticket.details = body.details
    ticket.status = body.status

    db.commit()
    db.refresh(ticket)

    return ticket


@router.delete("/{ticket_id}")
def delete_ticket(
    ticket_id: int,
    db: Session = Depends(get_db)
):
    ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id
    ).first()

    if not ticket:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    db.delete(ticket)
    db.commit()

    return {"message": "Ticket deleted"}