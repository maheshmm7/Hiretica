.PHONY: build up down logs test lint format

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

test:
	cd backend && pytest

lint:
	cd backend && flake8 . && mypy .
	cd frontend && npm run lint

format:
	cd backend && black . && isort .
