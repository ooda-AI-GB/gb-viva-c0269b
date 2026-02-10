FROM python:3.11-slim

WORKDIR /app

# Set environment variables for Python
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories
RUN mkdir -p data templates

# Copy application files
COPY main.py .
COPY templates/ templates/

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run the application
CMD ["python", "main.py"]
