# Project Tracking API

A REST API for tracking projects, teams, and template usage across an organization.

## Setup Instructions

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python project_tracking_api.py
```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, visit `http://localhost:8000/docs` for interactive API documentation (Swagger UI).

## Available Endpoints

### 1. Get All Projects
**GET** `/api/v1/projects`

Query Parameters:
- `status` (optional): Filter by status (active, maintenance, deprecated, archived)
- `limit` (optional): Maximum number of results (default: 50)

Example:
```
GET /api/v1/projects?status=active&limit=10
```

### 2. Get Project by Name
**GET** `/api/v1/projects/{project_name}`

Path Parameters:
- `project_name`: Full project name (e.g., "com.azure.TelemetryHub")

Example:
```
GET /api/v1/projects/com.azure.TelemetryHub
```

### 3. Get Projects by Team
**GET** `/api/v1/teams/{team_name}/projects`

Path Parameters:
- `team_name`: Team name (e.g., "Platform Engineering")

Example:
```
GET /api/v1/teams/Platform%20Engineering/projects
```

### 4. Get Projects by Template
**GET** `/api/v1/templates/{template_type}/projects`

Path Parameters:
- `template_type`: Template type (e.g., "microservice-basic")

Example:
```
GET /api/v1/templates/microservice-basic/projects
```

### 5. Get All Teams
**GET** `/api/v1/teams`

Returns statistics for all teams including project counts and templates used.

### 6. Get Statistics
**GET** `/api/v1/stats`

Returns overall statistics about projects and template usage.

## Response Examples

### Project Object
```json
{
  "project_id": "PROJ-1001",
  "project_name": "com.azure.TelemetryHub",
  "team_name": "Platform Engineering",
  "no_temps_used": 3,
  "templates": ["microservice-basic", "api-gateway", "event-driven"],
  "template_versions": ["2.1.5", "3.4.12", "1.8.23"],
  "last_updated": "2024-08-15",
  "status": "active",
  "repository_url": "https://github.com/company/com.azure.TelemetryHub",
  "created_date": "2023-03-22"
}
```

## Mock Data

The API uses a mock database with 50 pre-generated projects for testing purposes. Each project includes:
- Unique project ID and name
- Team assignment
- Template usage information
- Status and timestamps
- Repository URL

## Testing Considerations

This API is designed to be tested with various scenarios:
1. Valid and invalid project names
2. Team names with spaces
3. Case sensitivity handling
4. Non-existent resources (404 errors)
5. Query parameter validation
6. Different status filters
7. Limit parameter boundaries