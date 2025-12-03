FROM python:3.11-slim

WORKDIR /app

# Install UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files
COPY pyproject.toml ./

# Install dependencies
RUN uv pip install --system -e ".[dev]"

# Copy project files
COPY devices_manager/ ./devices_manager/

WORKDIR /app/devices_manager

# Expose port
EXPOSE 8000

CMD ["py", "manage.py", "runserver", "0.0.0.0:8000"]

