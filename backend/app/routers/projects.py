from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.project import ProjectListResponse, ProjectResponse
from app.services.project_service import get_all_projects

router = APIRouter(prefix="/api/projects", tags=["Projects"])

@router.get(
    "",
    response_model=ProjectListResponse,
    summary="List Featured Projects",
    description="Fetches all published portfolio projects with details, tech stack, and key features."
)
def list_projects(db: Session = Depends(get_db)):
    projects = get_all_projects(db)
    return ProjectListResponse(
        success=True,
        count=len(projects),
        data=[ProjectResponse.model_validate(p) for p in projects]
    )
