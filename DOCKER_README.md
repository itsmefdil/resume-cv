# Docker Setup for Resume Website

This directory contains Docker configuration for running the Flask resume website in both development and production environments.

## Quick Start

### Development Environment

```bash
# Build and start development environment
make dev

# Or manually:
docker-compose up -d

# Access the application at http://localhost:8001
```

### Production Environment

```bash
# Build and start production environment
make prod

# Or manually:
docker-compose -f docker-compose.prod.yml up -d

# Access the application at http://localhost
```

## Available Make Commands

- `make help` - Show available commands
- `make build` - Build development Docker image
- `make build-prod` - Build production Docker image
- `make up` - Start development environment
- `make up-prod` - Start production environment
- `make down` - Stop all containers
- `make logs` - Show container logs
- `make shell` - Access container shell
- `make clean` - Remove containers, images, and volumes
- `make restart` - Restart development services
- `make restart-prod` - Restart production services

## Environment Files

### Development (.env.dev)
- `FLASK_ENV=development`
- `FLASK_DEBUG=1`
- Hot reloading enabled
- Volume mounting for code changes

### Production (.env.prod)
- `FLASK_ENV=production`
- Gunicorn WSGI server
- Nginx reverse proxy
- Security headers
- Gzip compression

## Architecture

### Development Stack
- **Flask App**: Development server with hot reloading
- **Port**: 8001
- **Volume Mounting**: Code changes reflected immediately

### Production Stack
- **Flask App**: Gunicorn WSGI server (4 workers)
- **Nginx**: Reverse proxy with SSL termination
- **Port**: 80 (HTTP), 443 (HTTPS)
- **Features**: 
  - Load balancing
  - Static file serving
  - Gzip compression
  - Security headers
  - Rate limiting

## File Structure

```
├── Dockerfile              # Development Docker image
├── Dockerfile.prod         # Production Docker image
├── docker-compose.yml      # Development environment
├── docker-compose.prod.yml # Production environment
├── .dockerignore           # Docker ignore patterns
├── .env.dev               # Development environment variables
├── .env.prod              # Production environment variables
├── Makefile               # Docker management commands
└── nginx/
    ├── nginx.conf         # Nginx configuration
    └── ssl/               # SSL certificates (add your own)
```

## Customization

### Environment Variables

Copy and modify the environment files:

```bash
cp .env.dev .env.local
cp .env.prod .env.production
```

Edit the values according to your needs.

### SSL Configuration

For production HTTPS:

1. Add your SSL certificates to `nginx/ssl/`:
   - `cert.pem` (certificate)
   - `key.pem` (private key)

2. Uncomment the HTTPS server block in `nginx/nginx.conf`

3. Update the domain name in the configuration

### Production Deployment

1. Set production environment variables in `.env.prod`
2. Add SSL certificates if using HTTPS
3. Update `nginx/nginx.conf` with your domain
4. Deploy with: `make prod`

## Monitoring

### Health Checks

Both containers include health checks:
- Flask app: `GET /` (returns 200 for healthy)
- Nginx: Built-in health endpoint at `/health`

### Logs

```bash
# Development logs
make logs

# Production logs
make logs-prod

# Follow specific service logs
docker-compose logs -f web
```

### Container Status

```bash
# Check running containers
docker-compose ps

# Check container health
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

## Troubleshooting

### Common Issues

1. **Port already in use**:
   ```bash
   # Check what's using the port
   lsof -i :8001
   
   # Or change the port in docker-compose.yml
   ```

2. **Permission issues**:
   ```bash
   # Rebuild with no-cache
   docker-compose build --no-cache
   ```

3. **Static files not loading**:
   ```bash
   # Restart containers
   make restart
   ```

### Debugging

```bash
# Access container shell
make shell

# Check container logs
docker-compose logs web

# Inspect container
docker inspect resume-web-dev
```

## Security Considerations

### Development
- Uses non-root user inside container
- Debug mode enabled (disable in production)
- Volume mounting (development only)

### Production
- Nginx security headers
- Rate limiting
- SSL/TLS termination
- No debug information exposed
- Health checks enabled
- Resource limits (configure as needed)

## Performance Tuning

### Gunicorn Workers
Adjust workers in `.env.prod`:
```
WORKERS=4  # CPU cores * 2 + 1
```

### Nginx Configuration
- Gzip compression enabled
- Static file caching (1 year)
- Keep-alive connections
- Request rate limiting

## Backup and Data

### Volume Data
```bash
# Backup volumes
docker run --rm -v resume_data:/data -v $(pwd):/backup alpine tar czf /backup/backup.tar.gz -C /data .

# Restore volumes  
docker run --rm -v resume_data:/data -v $(pwd):/backup alpine tar xzf /backup/backup.tar.gz -C /data
```

## Updates and Maintenance

### Update Dependencies
```bash
# Update Python packages
pip freeze > requirements.txt

# Rebuild containers
make build
```

### Update Base Images
```bash
# Pull latest base images
docker pull python:3.11-slim
docker pull nginx:alpine

# Rebuild
make build
```
