FROM python:3.12-slim

# Set environment flags to prevent .pyc generation and ensure direct logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Security Hardening: Create a non-root system group and user
# Running as an unprivileged user limits damage if a container is compromised
RUN groupadd -r appgroup && \
    useradd -r -g appgroup -d /app -s /usr/sbin/nologin -c "App User" appuser

# Install Flask dependency
RUN pip install --no-cache-dir Flask==3.1.1

# Copy application source code and transfer ownership to the unprivileged user
COPY --chown=appuser:appgroup app.py .

# Switch from root to non-root application user
USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
