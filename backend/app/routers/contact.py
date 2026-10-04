import logging
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.contact import ContactCreate, ContactResponse
from app.services.contact_service import save_contact_message

logger = logging.getLogger("uvicorn.error")

router = APIRouter(prefix="/api/contact", tags=["Contact"])

@router.post(
    "",
    response_model=ContactResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit Contact Inquiry",
    description="Validates and persists a contact inquiry from the portfolio website into the database."
)
async def submit_contact(
    contact_data: ContactCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    try:
        # Extract client metadata for audit and rate-limiting
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")[:255]

        # Save to database
        saved_contact = save_contact_message(
            db=db,
            contact_in=contact_data,
            ip_address=client_ip,
            user_agent=user_agent
        )

        return ContactResponse(
            success=True,
            message="Thank you! Your message has been sent successfully. Vikas will get back to you soon.",
            contact_id=saved_contact.id,
            created_at=saved_contact.created_at
        )
    except Exception as e:
        logger.error(f"Error handling contact submission: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to submit your message. Please try again or reach out directly via email."
        )
