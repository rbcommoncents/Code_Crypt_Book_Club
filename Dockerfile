# Use Python base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files into the container
COPY . .

# Expose Django's default port
EXPOSE 8000

# Set environment variables for local development
ENV PYTHONUNBUFFERED=1 \
    DEBUG=True

# Run migrations and start Django without creating a superuser
CMD ["sh", "-c", "python wait_for_db.py && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
