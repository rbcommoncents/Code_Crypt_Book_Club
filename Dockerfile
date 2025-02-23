# Use latest Python version
FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Copy the project files into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Expose the application port
EXPOSE 8000

# Run migrations and start the application
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn --workers 3 --bind 0.0.0.0:8000 Coterie.wsgi:application"]
