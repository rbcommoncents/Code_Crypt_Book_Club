# **Django Web Application**

## **Overview**
The following is a Django-based web application designed for managing drink recipes, music, and artwork. It supports:
- **PostgreSQL** as the primary database.
- **AWS S3** for media storage (profile pictures, music, and videos).
- **Gunicorn** for WSGI production server.
- **Docker & Docker Compose** for containerized deployment.
- **SSL (HTTPS)** enforcement for secure web traffic.

---

## **System Requirements**
- Python **3.12+**
- PostgreSQL **12+**
- Docker & Docker Compose
- AWS S3 bucket for media storage

---

## **Installation & Setup**

### **1️⃣ Set Up Environment Variables**
Create a **`.env`** file in the root directory and add:

```ini
# PostgreSQL Configuration
POSTGRES_DB=coterie_db
POSTGRES_USER=coterie_user
POSTGRES_PASSWORD=securepassword
DB_HOST=db  # Use 'localhost' if running locally
DB_PORT=5432

# Django Configuration
DEBUG=False  # Set to True for local development
SECRET_KEY=your_secret_key_here
ALLOWED_HOSTS=127.0.0.1,localhost,your-domain.com

# AWS S3 Configuration (for storing media)
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_STORAGE_BUCKET_NAME=django-project-rizz
AWS_S3_REGION_NAME=us-east-2

# Docker Environment Detection
IS_DOCKER=True  # Set to True when running inside Docker

    🔹 Notes:

        Set DEBUG=False in production.
        Use DB_HOST=db inside Docker; use localhost when running locally.
        AWS credentials are required for media storage.

2️⃣ Running Locally (Without Docker)

python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runserver

3️⃣ Running with Docker

docker compose up --build -d

To stop:

docker compose down

4️⃣ Creating a Superuser for Django Admin

After running the application, create an admin user:

docker compose exec web python manage.py createsuperuser

Login at:

http://127.0.0.1:8000/admin/

Profile Picture & Media Handling

    User profile pictures are uploaded to AWS S3 in the profile_pics/ folder.
    Music & Videos are uploaded directly to AWS S3.
    Static files (CSS/JS/images) are handled via WhiteNoise.

    ✅ Profile pictures are uniquely named using UUID to avoid conflicts. ✅ All media is served securely over HTTPS.

API Authentication

    The application supports token-based authentication for admin users to access APIs.
    Admins can generate API Tokens from their Profile Page.
    All API requests require a Token header.

    Example API Request:

curl -X GET http://localhost:8000/api/drinks/ \
     -H "Authorization: Token your-api-token-here"

    Example API Token Generation:

docker compose exec web python manage.py drf_create_token your_admin_user

Enforcing SSL (HTTPS)

The application forces all traffic through HTTPS:

    Django Settings (settings.py)

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

Local SSL Testing (django-sslserver)

python manage.py runsslserver

Production SSL with Nginx If running behind Nginx, update your configuration:

    server {
        listen 80;
        server_name your-domain.com;
        
        location / {
            proxy_pass http://127.0.0.1:8000;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto https;
            proxy_set_header Host $host;
        }

        # Redirect HTTP to HTTPS
        if ($scheme = http) {
            return 301 https://$host$request_uri;
        }
    }

✅ Now, all traffic is secured via SSL.
Database Setup (PostgreSQL)

If running PostgreSQL locally, install and configure:
🔹 Install PostgreSQL

sudo apt update && sudo apt install postgresql postgresql-contrib

🔹 Create a Database & User

sudo -u postgres psql

CREATE DATABASE coterie_db;
CREATE USER coterie_user WITH PASSWORD 'securepassword';
ALTER ROLE coterie_user SET client_encoding TO 'utf8';
ALTER ROLE coterie_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE coterie_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE coterie_db TO coterie_user;

Exit:

\q

🔹 Verify Database Connection

pg_isready -h 127.0.0.1 -p 5432 -U coterie_user

Docker Setup & Deployment
1️⃣ Build & Run Containers

docker compose build --no-cache
docker compose up -d

2️⃣ Check Running Containers

docker ps

3️⃣ Stop and Remove Containers

docker compose down -v

Troubleshooting
1️⃣ Check Logs for Errors

docker compose logs web | tail -n 20

docker compose logs db | tail -n 20

2️⃣ Reset Database & Volumes

docker compose down -v
docker compose up --build -d

3️⃣ Verify AWS Media Storage

Check if files exist in AWS S3:

aws s3 ls s3://django-project-rizz/profile_pics/

Ensure media loads:

curl -I https://django-project-rizz.s3.us-east-2.amazonaws.com/profile_pics/sample.jpg

Contributors

    Developer: Ryszard Bialach II
    Version: 1.0.0