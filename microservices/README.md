# GoAround Microservices Architecture

This project has been converted from a monolithic Flask application to a microservices architecture.

## Architecture Overview

The application is now split into 4 main services:

### 1. **Authentication Service** (Port 5001)
- Handles user registration and login
- Manages user data and login tracking
- Endpoints: `/signup`, `/signin`, `/user/<id>`, `/admin/logins`

### 2. **Package Management Service** (Port 5002)
- Manages travel packages and places data
- CRUD operations for packages
- Endpoints: `/packages`, `/api/places`, `/static/images/*`

### 3. **Maps & Places Service** (Port 5003)
- Handles mapping functionality
- Geocoding and routing services
- GeoJSON data management
- Endpoints: `/geojson`, `/geocode`, `/route`, `/api/cities`, `/api/annotations`

### 4. **API Gateway** (Port 5000)
- Routes requests to appropriate microservices
- Serves frontend templates
- Acts as the main entry point for the application
- Proxies requests to backend services

## Quick Start

### Option 1: Using Docker Compose (Recommended)
```bash
# Navigate to microservices directory
cd microservices

# Start all services with Docker
docker-compose up -d

# View logs
docker-compose logs -f
```

### Option 2: Running Locally
```bash
# Navigate to microservices directory
cd microservices

# Run the startup script (Windows)
start-services.bat

# Or manually start each service in separate terminals:
# Terminal 1: cd auth-service && python app.py
# Terminal 2: cd package-service && python app.py  
# Terminal 3: cd maps-service && python app.py
# Terminal 4: cd api-gateway && python app.py
```

## Service URLs
- **Main Application**: http://localhost:5000
- **Auth Service**: http://localhost:5001
- **Package Service**: http://localhost:5002
- **Maps Service**: http://localhost:5003

## Database Setup
The services use a shared MySQL database. When using Docker Compose, the database is automatically created and configured.

For local development, ensure MySQL is running and update the database configuration in `shared/config.py`.

## Environment Variables
For production deployment, set these environment variables:
- `SECRET_KEY`: Flask secret key
- `DATABASE_URL`: MySQL connection string
- `ORS_API_KEY`: OpenRouteService API key (for routing functionality)

## Service Dependencies
```
API Gateway → Auth Service
API Gateway → Package Service  
API Gateway → Maps Service
Auth Service → MySQL Database
Package Service → MySQL Database
```

## Health Checks
Each service provides a health check endpoint at `/health`:
- http://localhost:5001/health (Auth)
- http://localhost:5002/health (Package)
- http://localhost:5003/health (Maps)
- http://localhost:5000/health (Gateway)

## Development

### Adding New Features
1. Identify which service should handle the new functionality
2. Add endpoints to the appropriate service
3. Update API Gateway to proxy requests if needed
4. Update frontend templates if required

### Service Communication
Services communicate through HTTP REST APIs. The API Gateway handles routing from frontend to backend services.

### Database Migrations
Database models are defined in `shared/database.py`. All services that need database access import from this shared module.

## Deployment

### Docker Deployment
```bash
docker-compose up -d --build
```

### Production Considerations
1. Use a reverse proxy (nginx) in front of the API Gateway
2. Set up proper environment variables
3. Use a managed database service
4. Implement proper logging and monitoring
5. Set up health checks and auto-scaling

## Troubleshooting

### Service Won't Start
- Check if ports are already in use
- Verify database connection
- Check service logs for error details

### Database Connection Issues
- Ensure MySQL is running
- Check database credentials in config
- Verify network connectivity between services

### Frontend Not Loading
- Check if API Gateway is running on port 5000
- Verify template and static file paths
- Check browser console for JavaScript errors

## Migration from Monolith

The original monolithic application (`app.py`) has been split as follows:
- User authentication → Auth Service
- Package management → Package Service
- Mapping functionality → Maps Service
- Frontend serving → API Gateway

All original functionality is preserved while gaining the benefits of microservices architecture:
- Independent scaling
- Technology diversity
- Fault isolation
- Team autonomy
- Easier maintenance and deployment