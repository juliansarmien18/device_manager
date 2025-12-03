.PHONY: help install migrate run test clean docker-up docker-down

help:
	@echo "Comandos disponibles:"
	@echo "  make install     - Instalar dependencias"
	@echo "  make migrate     - Ejecutar migraciones"
	@echo "  make run         - Ejecutar servidor de desarrollo"
	@echo "  make test        - Ejecutar tests"
	@echo "  make test-data   - Crear datos de prueba"
	@echo "  make clean       - Limpiar archivos temporales"
	@echo "  make docker-up   - Iniciar Docker Compose"
	@echo "  make docker-down - Detener Docker Compose"

install:
	cd devices_manager && uv pip install -e ".[dev]"

migrate:
	cd devices_manager && py manage.py migrate

run:
	cd devices_manager && py manage.py runserver

test:
	cd devices_manager && py -m pytest

test-data:
	cd devices_manager && py manage.py create_test_data

clean:
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +

docker-up:
	docker-compose up --build

docker-down:
	docker-compose down
