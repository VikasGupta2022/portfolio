import logging
from sqlalchemy.orm import Session
from app.models.project import Project

logger = logging.getLogger("uvicorn.error")

DEFAULT_PROJECTS = [
    {
        "title": "Product Management System",
        "slug": "product-management-system",
        "badge": "Laravel & MySQL",
        "description": "Comprehensive enterprise product management and inventory tracking web application built with Laravel and MySQL. Features full CRUD capabilities, SKU indexing, real-time inventory alerts, bulk data import/export, and image uploads with server-side validation.",
        "technologies": ["Laravel", "PHP", "MySQL", "Bootstrap 5", "JavaScript"],
        "features": [
            "Product CRUD operations with image upload & file validation",
            "SKU tracking with low-stock alerts & stock level indicators",
            "Server-side search, filtering, and pagination",
            "CSV & Excel bulk product import and export engine",
            "Role-based access control for inventory managers"
        ],
        "image_url": "images/project-product-mgmt.jpg",
        "github_url": "https://github.com/VikasGupta2022",
        "demo_url": "#",
        "display_order": 1,
        "is_published": True
    },
    {
        "title": "HRMS / Employee Management System",
        "slug": "hrms-employee-management-system",
        "badge": "Laravel & Enterprise",
        "description": "Robust Human Resource Management System engineered with Laravel & MySQL to automate employee lifecycle, attendance logs, timesheets, payroll calculations with tax and gratuity formulas, and comprehensive reporting.",
        "technologies": ["PHP", "Laravel", "MySQL", "Bootstrap 5", "JavaScript", "Chart.js"],
        "features": [
            "Full employee directory with role and department assignments",
            "Daily attendance & timesheet logging with hours calculation",
            "Automated payroll generation with bonus and deduction rules",
            "Gratuity computation engine and financial report exports",
            "Employee training records, leave requests, and approval workflows"
        ],
        "image_url": "images/project-hrms.jpg",
        "github_url": "https://github.com/VikasGupta2022",
        "demo_url": "#",
        "display_order": 2,
        "is_published": True
    },
    {
        "title": "Student Management System",
        "slug": "student-management-system",
        "badge": "Core PHP & MVC",
        "description": "Lightweight and high-efficiency student academic management portal constructed using Core PHP and MySQL with an MVC architecture pattern, offering course registration, attendance tracking, and reporting.",
        "technologies": ["Core PHP", "MySQL", "HTML5", "CSS3", "Bootstrap", "JavaScript"],
        "features": [
            "Student records and profiles with enrollment history",
            "Course catalog and academic curriculum management",
            "Attendance marking system with percentage calculators",
            "Contact info directory with guardian details",
            "Clean MVC architecture and SQL prepared statements"
        ],
        "image_url": "images/project-student-mgmt.jpg",
        "github_url": "https://github.com/VikasGupta2022",
        "demo_url": "#",
        "display_order": 3,
        "is_published": True
    },
    {
        "title": "High-Performance Python REST API",
        "slug": "python-fastapi-rest-api",
        "badge": "Python & FastAPI",
        "description": "Modern asynchronous RESTful microservice built with Python 3 and FastAPI, leveraging Pydantic v2 schemas for robust request validation, SQLAlchemy ORM with MySQL integration, and JWT authentication.",
        "technologies": ["Python", "FastAPI", "MySQL", "Pydantic", "SQLAlchemy", "Uvicorn"],
        "features": [
            "Asynchronous endpoints for high-throughput CRUD operations",
            "Strong data validation and automatic serialization with Pydantic v2",
            "Interactive Swagger/OpenAPI and ReDoc self-documenting APIs",
            "JWT-based authentication and role-based route guards",
            "Robust database pooling with transactional integrity"
        ],
        "image_url": "images/project-fastapi-api.jpg",
        "github_url": "https://github.com/VikasGupta2022",
        "demo_url": "#",
        "display_order": 4,
        "is_published": True
    }
]

def seed_default_projects(db: Session):
    """
    Seeds initial default projects into the database if empty.
    """
    try:
        count = db.query(Project).count()
        if count == 0:
            logger.info("🌱 Seeding default projects into database...")
            for proj_data in DEFAULT_PROJECTS:
                project = Project(**proj_data)
                db.add(project)
            db.commit()
            logger.info("✅ Projects seeded successfully!")
    except Exception as e:
        db.rollback()
        logger.warning(f"⚠️ Project seeding skipped or failed: {e}")

def get_all_projects(db: Session) -> list[Project]:
    """
    Returns all published projects ordered by display_order.
    """
    return db.query(Project).filter(Project.is_published == True).order_by(Project.display_order.asc()).all()
