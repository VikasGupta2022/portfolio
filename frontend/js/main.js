/**
 * Vikas Gupta - Portfolio JavaScript Engine
 * Handles dynamic project loading, contact API communications,
 * project filters, modals, and smooth UI animations.
 */

// Determine backend API Base URL dynamically
// When served over HTTP/HTTPS (locally or cloud), relative paths hit the FastAPI backend directly
const API_BASE_URL = (window.location.protocol === "file:")
    ? "http://127.0.0.1:8000"
    : "";

// Fallback project data if API is offline
const STATIC_PROJECTS = [
  {
    id: 1,
    title: "Product Management System",
    slug: "product-management-system",
    badge: "Laravel / PHP",
    category: "laravel",
    description: "Enterprise product catalog and inventory tracking web application built with Laravel and MySQL. Engineered with bulk CSV/Excel import-export, SKU tracking, automated stock alerts, and server-side validation.",
    technologies: ["Laravel", "PHP", "MySQL", "Bootstrap 5", "JavaScript"],
    features: [
      "Product CRUD operations with image upload & file validation",
      "SKU tracking with low-stock alerts & stock level indicators",
      "Server-side search, filtering, and pagination",
      "CSV & Excel bulk product import and export engine",
      "Role-based access control for inventory managers"
    ],
    image_url: "images/project-product-mgmt.jpg",
    github_url: "https://github.com/VikasGupta2022",
    demo_url: "#"
  },
  {
    id: 2,
    title: "HRMS / Employee Management System",
    slug: "hrms-employee-management-system",
    badge: "Laravel / Enterprise",
    category: "laravel",
    description: "Comprehensive Human Resource Management System engineered with Laravel & MySQL to automate employee lifecycle, attendance logs, timesheets, payroll calculations with tax and gratuity formulas, and reporting.",
    technologies: ["PHP", "Laravel", "MySQL", "Bootstrap 5", "JavaScript", "Chart.js"],
    features: [
      "Full employee directory with role and department assignments",
      "Daily attendance & timesheet logging with hours calculation",
      "Automated payroll generation with bonus and deduction rules",
      "Gratuity computation engine and financial report exports",
      "Employee training records, leave requests, and approval workflows"
    ],
    image_url: "images/project-hrms.jpg",
    github_url: "https://github.com/VikasGupta2022",
    demo_url: "#"
  },
  {
    id: 3,
    title: "Student Management System",
    slug: "student-management-system",
    badge: "Core PHP / Portal",
    category: "php",
    description: "Lightweight and high-efficiency student academic management portal constructed using Core PHP and MySQL with an MVC architecture pattern, offering course registration, attendance tracking, and reporting.",
    technologies: ["Core PHP", "MySQL", "HTML5", "CSS3", "Bootstrap", "JavaScript"],
    features: [
      "Student records and profiles with enrollment history",
      "Course catalog and academic curriculum management",
      "Attendance marking system with percentage calculators",
      "Contact info directory with guardian details",
      "Clean MVC architecture and SQL prepared statements"
    ],
    image_url: "images/project-student-mgmt.jpg",
    github_url: "https://github.com/VikasGupta2022",
    demo_url: "#"
  },
  {
    id: 4,
    title: "High-Performance Python REST API",
    slug: "python-fastapi-rest-api",
    badge: "Python / FastAPI",
    category: "python",
    description: "Modern asynchronous RESTful microservice built with Python 3 and FastAPI, leveraging Pydantic v2 schemas for robust request validation, SQLAlchemy ORM with MySQL integration, and JWT authentication.",
    technologies: ["Python", "FastAPI", "MySQL", "Pydantic", "SQLAlchemy", "Uvicorn"],
    features: [
      "Asynchronous endpoints for high-throughput CRUD operations",
      "Strong data validation and automatic serialization with Pydantic v2",
      "Interactive Swagger/OpenAPI and ReDoc self-documenting APIs",
      "JWT-based authentication and role-based route guards",
      "Robust database pooling with transactional integrity"
    ],
    image_url: "images/project-fastapi-api.jpg",
    github_url: "https://github.com/VikasGupta2022",
    demo_url: "#"
  }
];

let allProjectsData = [...STATIC_PROJECTS];

document.addEventListener("DOMContentLoaded", () => {
  initNavbarScroll();
  initContactForm();
  loadProjects();
  initProjectFilters();
  initBackendStatusCheck();
});

/**
 * Navbar background shadow transition on scroll
 */
function initNavbarScroll() {
  const navbar = document.querySelector(".navbar-custom");
  window.addEventListener("scroll", () => {
    if (window.scrollY > 40) {
      navbar.classList.add("scrolled");
    } else {
      navbar.classList.remove("scrolled");
    }
  });
}

/**
 * Fetch projects from FastAPI backend or fallback gracefully
 */
async function loadProjects() {
  const container = document.getElementById("projects-grid-container");
  if (!container) return;

  try {
    const res = await fetch(`${API_BASE_URL}/api/projects`, { method: "GET" });
    if (res.ok) {
      const json = await res.json();
      if (json.data && json.data.length > 0) {
        allProjectsData = json.data.map(p => ({
          ...p,
          category: p.technologies.some(t => t.toLowerCase().includes("python")) ? "python" :
                    p.technologies.some(t => t.toLowerCase().includes("laravel")) ? "laravel" : "php"
        }));
      }
    }
  } catch (err) {
    console.info("Using embedded project dataset (FastAPI offline or direct local file execution).");
  }

  renderProjects(allProjectsData);
}

/**
 * Render Project Cards into DOM
 */
function renderProjects(projects) {
  const container = document.getElementById("projects-grid-container");
  if (!container) return;

  container.innerHTML = "";

  projects.forEach(project => {
    const isPython = project.technologies.some(t => t.toLowerCase().includes("python"));
    const badgeClass = isPython ? "project-badge-pill python-badge" : "project-badge-pill";

    const techTagsHtml = project.technologies
      .map(t => `<span class="tech-tag">${escapeHtml(t)}</span>`)
      .join("");

    const featuresHtml = project.features
      .slice(0, 3)
      .map(f => `<li>${escapeHtml(f)}</li>`)
      .join("");

    const cardCol = document.createElement("div");
    cardCol.className = `col-lg-6 col-md-12 mb-4 project-item-col`;
    cardCol.setAttribute("data-category", project.category || "all");

    cardCol.innerHTML = `
      <div class="project-card">
        <div class="project-img-wrap">
          <img src="${project.image_url}" alt="${escapeHtml(project.title)} Screenshot" class="project-img" loading="lazy" onerror="this.src='https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=800&q=80'">
          <span class="${badgeClass}">${escapeHtml(project.badge || 'Project')}</span>
        </div>
        <div class="project-body">
          <h3 class="project-title">${escapeHtml(project.title)}</h3>
          <p class="project-desc">${escapeHtml(project.description)}</p>
          <ul class="project-feature-list">
            ${featuresHtml}
          </ul>
          <div class="project-tech-tags">
            ${techTagsHtml}
          </div>
          <div class="project-footer-actions">
            <button class="btn btn-sm btn-outline-custom" onclick="openProjectModal('${project.slug}')">
              <i class="bi bi-info-circle me-1"></i> Details
            </button>
            <a href="${project.github_url || 'https://github.com/VikasGupta2022'}" target="_blank" rel="noopener noreferrer" class="btn btn-sm btn-outline-custom">
              <i class="bi bi-github me-1"></i> GitHub
            </a>
            ${isPython ? `
              <a href="${API_BASE_URL}/docs" target="_blank" rel="noopener noreferrer" class="btn btn-sm btn-primary-custom ms-auto">
                <i class="bi bi-lightning-charge me-1"></i> Swagger Docs
              </a>
            ` : `
              <a href="${project.demo_url || '#'}" target="_blank" rel="noopener noreferrer" class="btn btn-sm btn-primary-custom ms-auto ${project.demo_url === '#' ? 'disabled' : ''}">
                <i class="bi bi-box-arrow-up-right me-1"></i> Live Demo
              </a>
            `}
          </div>
        </div>
      </div>
    `;

    container.appendChild(cardCol);
  });
}

/**
 * Filter projects by category tab
 */
function initProjectFilters() {
  const filterBtns = document.querySelectorAll(".filter-btn");
  filterBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      filterBtns.forEach(b => b.classList.remove("active", "btn-primary-custom"));
      filterBtns.forEach(b => b.classList.add("btn-outline-custom"));
      
      btn.classList.remove("btn-outline-custom");
      btn.classList.add("active", "btn-primary-custom");

      const filterVal = btn.getAttribute("data-filter");
      if (filterVal === "all") {
        renderProjects(allProjectsData);
      } else {
        const filtered = allProjectsData.filter(p => p.category === filterVal);
        renderProjects(filtered);
      }
    });
  });
}

/**
 * Project Details Modal
 */
function openProjectModal(slug) {
  const project = allProjectsData.find(p => p.slug === slug);
  if (!project) return;

  const modalTitle = document.getElementById("projectModalLabel");
  const modalBody = document.getElementById("projectModalBody");

  modalTitle.textContent = project.title;

  const allFeaturesHtml = project.features
    .map(f => `<li class="mb-2"><i class="bi bi-check2-circle text-success me-2"></i>${escapeHtml(f)}</li>`)
    .join("");

  const techBadgesHtml = project.technologies
    .map(t => `<span class="badge bg-secondary me-1 mb-1 p-2 font-mono">${escapeHtml(t)}</span>`)
    .join("");

  modalBody.innerHTML = `
    <div class="mb-3 text-center">
      <img src="${project.image_url}" class="img-fluid rounded border border-secondary" alt="${escapeHtml(project.title)}">
    </div>
    <div class="mb-3">
      <span class="badge bg-info text-dark mb-2">${escapeHtml(project.badge)}</span>
      <p class="text-light">${escapeHtml(project.description)}</p>
    </div>
    <div class="mb-3">
      <h6 class="text-white fw-bold">Key Architectural Features:</h6>
      <ul class="list-unstyled text-muted small">
        ${allFeaturesHtml}
      </ul>
    </div>
    <div class="mb-3">
      <h6 class="text-white fw-bold">Technologies Employed:</h6>
      <div>${techBadgesHtml}</div>
    </div>
    <div class="d-flex gap-2 justify-content-end pt-3 border-top border-secondary">
      <a href="${project.github_url || 'https://github.com/VikasGupta2022'}" target="_blank" class="btn btn-outline-light btn-sm">
        <i class="bi bi-github me-1"></i> Repository
      </a>
      <button type="button" class="btn btn-primary-custom btn-sm" data-bs-dismiss="modal">Close</button>
    </div>
  `;

  const modalEl = document.getElementById("projectDetailModal");
  if (modalEl && window.bootstrap) {
    const modal = new bootstrap.Modal(modalEl);
    modal.show();
  }
}

/**
 * Contact Form Submit to Python FastAPI Backend
 */
function initContactForm() {
  const form = document.getElementById("contactForm");
  const alertContainer = document.getElementById("contactAlert");
  const submitBtn = document.getElementById("contactSubmitBtn");

  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    // Reset alert
    alertContainer.innerHTML = "";
    alertContainer.className = "d-none";

    const nameInput = document.getElementById("contactName");
    const emailInput = document.getElementById("contactEmail");
    const subjectInput = document.getElementById("contactSubject");
    const messageInput = document.getElementById("contactMessage");

    const payload = {
      name: nameInput.value.trim(),
      email: emailInput.value.trim(),
      subject: subjectInput.value.trim(),
      message: messageInput.value.trim()
    };

    // Client-side quick validation
    if (!payload.name || payload.name.length < 2) {
      showAlert(alertContainer, "danger", "Please provide your name (at least 2 characters).");
      nameInput.focus();
      return;
    }
    if (!validateEmail(payload.email)) {
      showAlert(alertContainer, "danger", "Please provide a valid email address.");
      emailInput.focus();
      return;
    }
    if (!payload.subject || payload.subject.length < 3) {
      showAlert(alertContainer, "danger", "Please enter a subject (at least 3 characters).");
      subjectInput.focus();
      return;
    }
    if (!payload.message || payload.message.length < 10) {
      showAlert(alertContainer, "danger", "Please enter a detailed message (at least 10 characters).");
      messageInput.focus();
      return;
    }

    // Set loading button state
    const originalBtnText = submitBtn.innerHTML;
    submitBtn.disabled = true;
    submitBtn.innerHTML = `<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span> Transmitting via FastAPI...`;

    try {
      const response = await fetch(`${API_BASE_URL}/api/contact`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Accept": "application/json"
        },
        body: JSON.stringify(payload)
      });

      const data = await response.json();

      if (response.ok && data.success) {
        showAlert(alertContainer, "success", `
          <strong>Message Received!</strong> ${data.message} 
          <br><small class="text-white-50">Reference ID: #${data.contact_id || 'CONFIRMED'} • Stored in Database</small>
        `);
        form.reset();
      } else {
        // Validation error from Pydantic or server
        let errorMsg = "Unable to process your message at this time.";
        if (data.detail) {
          if (Array.isArray(data.detail)) {
            errorMsg = data.detail.map(d => d.msg || d.message).join(", ");
          } else {
            errorMsg = data.detail;
          }
        }
        showAlert(alertContainer, "danger", `<strong>Submission Error:</strong> ${escapeHtml(errorMsg)}`);
      }
    } catch (err) {
      console.error("Contact API Network Error:", err);
      showAlert(alertContainer, "warning", `
        <strong>FastAPI Backend Offline:</strong> The backend API server is currently not reachable at <code>${API_BASE_URL || window.location.origin}</code>. 
        Please start the server with <code>python run_backend.py</code> or email directly at <a href="mailto:vikasgupta2020vg@gmail.com" class="text-white text-decoration-underline">vikasgupta2020vg@gmail.com</a>.
      `);
    } finally {
      submitBtn.disabled = false;
      submitBtn.innerHTML = originalBtnText;
    }
  });
}

function showAlert(container, type, messageHtml) {
  container.className = `alert alert-${type} alert-dismissible fade show mt-3 border-0 shadow-sm`;
  container.innerHTML = `
    <div>${messageHtml}</div>
    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="alert" aria-label="Close"></button>
  `;
}

function validateEmail(email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(String(email).toLowerCase());
}

function escapeHtml(text) {
  if (!text) return "";
  const map = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#039;'
  };
  return String(text).replace(/[&<>"']/g, m => map[m]);
}

/**
 * Health check on startup to show API status badge
 */
async function initBackendStatusCheck() {
  const statusEl = document.getElementById("backend-status-pill");
  if (!statusEl) return;

  try {
    const res = await fetch(`${API_BASE_URL}/api/health`, { method: "GET" });
    if (res.ok) {
      const data = await res.json();
      statusEl.innerHTML = `<span class="badge bg-success font-mono"><i class="bi bi-cpu-fill me-1"></i>FastAPI Active (${data.database_backend.toUpperCase()})</span>`;
    } else {
      statusEl.innerHTML = `<span class="badge bg-secondary font-mono">FastAPI Standby</span>`;
    }
  } catch (e) {
    statusEl.innerHTML = `<span class="badge bg-secondary font-mono">FastAPI Standby</span>`;
  }
}
