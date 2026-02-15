from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
from datetime import datetime, timedelta
import random
import uvicorn

app = FastAPI(
    title="Project Tracking API",
    description="API for tracking projects, teams, and template usage across the organization",
    version="1.0.0"
)

# Mock data constants
PROJECT_PREFIXES = [
    "com.azure", "com.aws", "com.googlecloud", "com.meta",
    "io.github", "io.gitlab", "io.npm", "io.pydata",
    "dev.startup", "dev.internal", "tech.core", "cloud.edge",
    "ai.research", "ml.pipeline", "data.lakehouse", "platform.api",
    "infra.services", "core.backend", "frontend.webapp", "security.auth"
]

PROJECT_NAMES = [
    "TelemetryHub", "DataForge", "Streamline", "PulseSync",
    "VectorFlow", "NimbusCore", "QuantumMesh", "CircuitDash",
    "OpsCenter", "DeployMate", "ClusterPilot", "SentryGrid",
    "LogHarbor", "CacheBoost", "NeuraLinker", "APIBridge",
    "EventStream", "ConfigMaster", "ShardManager", "TaskRunner",
    "GraphPulse", "ModelRegistry", "KeyVault", "TraceRouter",
    "LoadBalancerX", "SessionStore", "QueueWorker", "PipelineOrchestrator"
]

TEAM_NAMES = [
    "Platform Engineering",
    "Cloud Infrastructure",
    "DevOps Guild",
    "API Services Team",
    "Observability Squad",
    "Data Engineering",
    "Site Reliability Group",
    "Frontend Systems",
    "Backend Services",
    "AI/ML Research Unit",
    "Security Engineering",
    "Automation Crew",
    "Release Management",
    "Integration Services",
    "Edge Compute Team",
    "Developer Experience",
    "Mobile Engineering",
    "Core Services",
    "Identity & Access",
    "Payments Platform",
    "Search & Indexing",
    "Analytics Pipeline",
    "Content Delivery",
    "Incident Response Team"
]

TEMPLATE_TYPES = [
    "microservice-basic",
    "microservice-advanced",
    "monolith-web",
    "serverless-function",
    "data-pipeline",
    "ml-training",
    "frontend-react",
    "frontend-vue",
    "api-gateway",
    "event-driven"
]

# Helper functions
def random_version():
    major = random.randint(1, 5)
    minor = random.randint(0, 20)
    patch = random.randint(0, 50)
    return f"{major}.{minor}.{patch}"

def random_date():
    start_date = datetime.now() - timedelta(days=730)
    random_days = random.randint(0, 730)
    return (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d")

def generate_project_data(count=50):
    projects = []
    for i in range(count):
        prefix = random.choice(PROJECT_PREFIXES)
        name = random.choice(PROJECT_NAMES)
        full_project_name = f"{prefix}.{name}"
        
        num_templates = random.randint(1, 5)
        templates_used = random.sample(TEMPLATE_TYPES, min(num_templates, len(TEMPLATE_TYPES)))
        
        project = {
            "project_id": f"PROJ-{1000 + i}",
            "project_name": full_project_name,
            "team_name": random.choice(TEAM_NAMES),
            "no_temps_used": num_templates,
            "templates": templates_used,
            "template_versions": [random_version() for _ in range(num_templates)],
            "last_updated": random_date(),
            "status": random.choice(["active", "maintenance", "deprecated", "archived"]),
            "repository_url": f"https://github.com/company/{full_project_name}",
            "created_date": random_date()
        }
        projects.append(project)
    return projects

# Generate mock database
MOCK_DATABASE = generate_project_data(50)

# API Endpoints

@app.get("/")
def root():
    return {
        "message": "Project Tracking API",
        "version": "1.0.0",
        "endpoints": [
            "/api/v1/projects",
            "/api/v1/projects/{project_name}",
            "/api/v1/teams/{team_name}/projects",
            "/api/v1/templates/{template_type}/projects"
        ]
    }

@app.get("/api/v1/projects")
def get_all_projects(
    status: Optional[str] = Query(None, description="Filter by project status"),
    limit: Optional[int] = Query(50, description="Maximum number of projects to return")
):
    """
    Get all projects with optional filtering by status
    """
    filtered_projects = MOCK_DATABASE
    
    if status:
        filtered_projects = [p for p in filtered_projects if p["status"] == status]
    
    return {
        "total": len(filtered_projects),
        "limit": limit,
        "projects": filtered_projects[:limit]
    }

@app.get("/api/v1/projects/{project_name}")
def get_project_by_name(project_name: str):
    """
    Get a specific project by its full name (e.g., com.azure.TelemetryHub)
    """
    for project in MOCK_DATABASE:
        if project["project_name"].lower() == project_name.lower():
            return project
    
    raise HTTPException(status_code=404, detail=f"Project '{project_name}' not found")

@app.get("/api/v1/teams/{team_name}/projects")
def get_projects_by_team(team_name: str):
    """
    Get all projects belonging to a specific team
    """
    team_projects = [p for p in MOCK_DATABASE if p["team_name"].lower() == team_name.lower()]
    
    if not team_projects:
        raise HTTPException(status_code=404, detail=f"No projects found for team '{team_name}'")
    
    return {
        "team_name": team_name,
        "project_count": len(team_projects),
        "projects": team_projects
    }

@app.get("/api/v1/templates/{template_type}/projects")
def get_projects_by_template(template_type: str):
    """
    Get all projects using a specific template type
    """
    template_projects = [
        p for p in MOCK_DATABASE 
        if template_type.lower() in [t.lower() for t in p["templates"]]
    ]
    
    if not template_projects:
        raise HTTPException(
            status_code=404, 
            detail=f"No projects found using template '{template_type}'"
        )
    
    return {
        "template_type": template_type,
        "project_count": len(template_projects),
        "projects": template_projects
    }

@app.get("/api/v1/teams")
def get_all_teams():
    """
    Get a list of all teams and their project counts
    """
    team_stats = {}
    for project in MOCK_DATABASE:
        team = project["team_name"]
        if team not in team_stats:
            team_stats[team] = {
                "team_name": team,
                "project_count": 0,
                "active_projects": 0,
                "templates_used": set()
            }
        team_stats[team]["project_count"] += 1
        if project["status"] == "active":
            team_stats[team]["active_projects"] += 1
        for template in project["templates"]:
            team_stats[team]["templates_used"].add(template)
    
    # Convert sets to lists for JSON serialization
    for team in team_stats.values():
        team["templates_used"] = list(team["templates_used"])
    
    return {
        "total_teams": len(team_stats),
        "teams": list(team_stats.values())
    }

@app.get("/api/v1/stats")
def get_statistics():
    """
    Get overall statistics about projects and templates
    """
    total_projects = len(MOCK_DATABASE)
    active_projects = sum(1 for p in MOCK_DATABASE if p["status"] == "active")
    
    template_usage = {}
    for project in MOCK_DATABASE:
        for template in project["templates"]:
            template_usage[template] = template_usage.get(template, 0) + 1
    
    return {
        "total_projects": total_projects,
        "active_projects": active_projects,
        "archived_projects": sum(1 for p in MOCK_DATABASE if p["status"] == "archived"),
        "deprecated_projects": sum(1 for p in MOCK_DATABASE if p["status"] == "deprecated"),
        "total_teams": len(set(p["team_name"] for p in MOCK_DATABASE)),
        "template_usage": template_usage,
        "most_used_template": max(template_usage.items(), key=lambda x: x[1])[0] if template_usage else None
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)