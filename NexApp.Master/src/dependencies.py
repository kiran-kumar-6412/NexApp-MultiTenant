from sqlalchemy.orm import Session
from src.database import local_session


def get_db():
    db: Session = local_session()
    try:
        yield db
    except Exception as e:
        from src.utils import logger
        logger.logging_error(f"Database error: {e}")  # ✅ Log the error
        raise  # ✅ Re-raise the exception to avoid silent failures
    finally:
        db.close()
