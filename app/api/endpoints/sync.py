from fastapi import APIRouter
from sqlmodel import Session, select
from app.db.models import ConditionsSet, ConditonsSetPublic, EventSet, EventPublic
from app.db.session import engine
from datetime import datetime

router = APIRouter()

@router.get("/synchronize-data")
def synchronize_data():
    with Session(engine) as session:
        # Pobierz niesynchronizowane rekordy
        unsynced_conditions = session.exec(
            select(ConditionsSet).where(ConditionsSet.synced == False)
        ).all()

        unsynced_events = session.exec(
            select(EventSet).where(EventSet.synced == False)
        ).all()

        # Oznacz jako zsynchronizowane
        for item in unsynced_conditions + unsynced_events:
            item.synced = True
        session.commit()

        # Zwróć dane w postaci publicznej
        conditions_out = [ConditonsSetPublic.from_orm(obj) for obj in unsynced_conditions]
        events_out = [EventPublic.from_orm(obj) for obj in unsynced_events]

        return {
            "conditions": conditions_out,
            "events": events_out,
            "date": datetime.now().astimezone()
        }
