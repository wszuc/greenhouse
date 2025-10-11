from sqlmodel import Session
from app.db.session import engine
from app.db.models import EventSet
from app.db.init_db import init_db


def log_system_event(info: str, uid: str = "raspberry") -> bool:
    """
    Log a system event to dedicated database.

    Args:
        info: Opis zdarzenia (np. 'Watering turned ON')
        uid: Identyfikator urządzenia (domyślnie 'raspberry')

    Returns:
        bool: True jeśli zapis się udał, False w razie błędu
    """
    try:
        init_db()

        with Session(engine) as session:
            new_event = EventSet(info=info, uid=uid)
            session.add(new_event)
            session.commit()
            print(f"[EVENT LOG] {info}")
            return True

    except Exception as e:
        print(f"[ERROR] Failed to log system event: {e}")
        return False
