import logging
from sqlalchemy.orm import Session
from app.models.contact import Contact
from app.schemas.contact import ContactCreate

logger = logging.getLogger("uvicorn.error")

def save_contact_message(
    db: Session,
    contact_in: ContactCreate,
    ip_address: str | None = None,
    user_agent: str | None = None
) -> Contact:
    """
    Saves a validated contact inquiry to the database.
    """
    try:
        new_contact = Contact(
            name=contact_in.name,
            email=contact_in.email,
            subject=contact_in.subject,
            message=contact_in.message,
            ip_address=ip_address,
            user_agent=user_agent
        )
        db.add(new_contact)
        db.commit()
        db.refresh(new_contact)
        logger.info(f"📨 New contact message received from {contact_in.email} (ID: {new_contact.id})")
        return new_contact
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Error saving contact message: {e}")
        raise e
