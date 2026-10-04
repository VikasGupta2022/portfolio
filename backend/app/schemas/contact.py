from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator
import html

class ContactCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Sender's full name")
    email: EmailStr = Field(..., description="Valid contact email address")
    subject: str = Field(..., min_length=3, max_length=200, description="Subject of the message")
    message: str = Field(..., min_length=10, max_length=3000, description="Message body")

    @field_validator("name", "subject", "message")
    @classmethod
    def sanitize_strings(cls, v: str) -> str:
        # Strip leading/trailing whitespaces and escape potentially unsafe HTML
        cleaned = v.strip()
        if not cleaned:
            raise ValueError("Field cannot be empty or solely whitespace")
        # Sanitize HTML tags to prevent XSS injection
        return html.escape(cleaned)

class ContactResponse(BaseModel):
    success: bool
    message: str
    contact_id: int | None = None
    created_at: datetime | None = None

    class Config:
        from_attributes = True
