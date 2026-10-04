from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON
from app.database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(150), nullable=False)
    slug = Column(String(160), unique=True, index=True, nullable=False)
    badge = Column(String(50), default="Full-Stack")
    description = Column(Text, nullable=False)
    technologies = Column(JSON, nullable=False)  # List of strings e.g. ["Laravel", "PHP"]
    features = Column(JSON, nullable=False)      # List of strings
    image_url = Column(String(255), nullable=True)
    github_url = Column(String(255), nullable=True)
    demo_url = Column(String(255), nullable=True)
    display_order = Column(Integer, default=0)
    is_published = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Project(id={self.id}, title='{self.title}')>"
