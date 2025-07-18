# Resume Website Docker Management

.PHONY: help build build-prod up up-prod down logs shell clean

# Default target
help:
	@echo "Available commands:"
	@echo "  build      - Build development Docker image"
	@echo "  build-prod - Build production Docker image"
	@echo "  up         - Start development environment"
	@echo "  up-prod    - Start production environment"
	@echo "  down       - Stop all containers"
	@echo "  logs       - Show container logs"
	@echo "  shell      - Access container shell"
	@echo "  clean      - Remove containers, images, and volumes"
	@echo "  test       - Run tests in container"

# Development commands
build:
	docker-compose build

up:
	docker-compose up -d
	@echo "Development server running at http://localhost:8001"

# Production commands
build-prod:
	docker-compose -f docker-compose.prod.yml build

up-prod:
	docker-compose -f docker-compose.prod.yml up -d
	@echo "Production server running at http://localhost"

# Common commands
down:
	docker-compose down
	docker-compose -f docker-compose.prod.yml down

logs:
	docker-compose logs -f

logs-prod:
	docker-compose -f docker-compose.prod.yml logs -f

shell:
	docker-compose exec web bash

shell-prod:
	docker-compose -f docker-compose.prod.yml exec web bash

# Cleanup commands
clean:
	docker-compose down -v --rmi all --remove-orphans
	docker-compose -f docker-compose.prod.yml down -v --rmi all --remove-orphans
	docker system prune -f

# Test command
test:
	docker-compose exec web python -m pytest

# Development workflow
dev: build up
	@echo "Development environment is ready!"

# Production workflow  
prod: build-prod up-prod
	@echo "Production environment is ready!"

# Restart services
restart:
	docker-compose restart

restart-prod:
	docker-compose -f docker-compose.prod.yml restart
