from datetime import datetime
from pydantic import BaseModel, Field

class ProjectBase(BaseModel):
    title: str = Field(..., max_length=150)
    slug: str = Field(..., max_length=160)
    badge: str = Field(default="Full-Stack", max_length=50)
    description: str
    technologies: list[str]
    features: list[str]
    image_url: str | None = None
    github_url: str | None = None
    demo_url: str | None = None
    display_order: int = 0

class ProjectResponse(ProjectBase):
    id: int
    is_published: bool
    created_at: datetime

    class Config:
        from_attributes = True

class ProjectListResponse(BaseModel):
    success: bool
    count: int
    data: list[ProjectResponse]
