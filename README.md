### **README.md**
# Coterie Web Application

## Project Overview
Coterie is a Django-based web application designed for managing drink recipes. It supports **PostgreSQL** as its database backend and provides both **local and Docker-based** development environments.

# Docker Installation Guide (Ubuntu)
This guide provides step-by-step instructions for installing and verifying Docker on Ubuntu.

---

## 1. Prerequisites
Ensure your system is **Ubuntu 22.04+** (or a compatible version). Check with:
```bash
lsb_release -a
```

---

## 2. Install Docker
### Step 1: Add Docker’s GPG Key
```bash
sudo mkdir -p /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor --yes -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
```

### Step 2: Add the Docker Repository
```bash
echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/docker.gpg] \
https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | \
sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

### Step 3: Update Package List
```bash
sudo apt update
```

### Step 4: Install Docker
```bash
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

---

## 3. Verify Installation
Check Docker version:
```bash
docker --version
```

Run a test container:
```bash
sudo docker run hello-world
```

---

## 4. (Optional) Run Docker Without `sudo`
To avoid using `sudo` with Docker, add your user to the Docker group:
```bash
sudo usermod -aG docker $USER
newgrp docker
```
Log out and back in for changes to apply.

---

## 5. Next Steps
- **List running containers:** `docker ps -a`  
- **Run an interactive container:** `docker run -it ubuntu bash`  
- **Check Docker Compose version:** `docker compose version`  

---

## Installation & Setup

### System Requirements
- Python **3.10+**
- PostgreSQL **12+**
- Docker & Docker Compose
- Virtual Environment (optional for local development)

---

## Setting Up PostgreSQL
If you are running PostgreSQL **locally** (instead of Docker), follow these steps.

### Install PostgreSQL
#### Linux (Debian/Ubuntu)
```sh
sudo apt update && sudo apt install postgresql postgresql-contrib
```
#### macOS (Homebrew)
```sh
brew install postgresql
brew services start postgresql
```
#### Windows
Download & install from [PostgreSQL Official Site](https://www.postgresql.org/download/).

### Create a PostgreSQL User & Database
Run the following:
```sh
sudo -u postgres psql
```
Inside PostgreSQL, create a user and database:
```sql
CREATE DATABASE coterie_db;
CREATE USER coterie_user WITH PASSWORD 'securepassword';
ALTER ROLE coterie_user SET client_encoding TO 'utf8';
ALTER ROLE coterie_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE coterie_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE coterie_db TO coterie_user;
```
Exit PostgreSQL:
```sql
\q
```

### Configure `pg_hba.conf` for Local & External Connections
The **pg_hba.conf** file controls how clients authenticate to PostgreSQL. Open it:
```sh
sudo nano /etc/postgresql/12/main/pg_hba.conf
```
(If using a different version, change `12` to your PostgreSQL version.)

#### Update Authentication Rules
Add or modify the following lines:
```
# TYPE  DATABASE        USER            ADDRESS                 METHOD
local   all             postgres                                md5
host    all             postgres        127.0.0.1/32            md5
host    all             postgres        ::1/128                 md5
host    all             all             0.0.0.0/0               md5  # Allow external connections
```
Save the file (**Ctrl+X → Y → Enter**) and restart PostgreSQL:
```sh
sudo systemctl restart postgresql
```
To verify, run:
```sh
pg_isready -h 127.0.0.1 -p 5432 -U coterie_user
```

---

## Setting Up Environment Variables (`.env`)

If you're forking this project from GitHub, create a **`.env`** file in the root directory and add the following:

### Example `.env` File
```ini
# Database Configuration
POSTGRES_DB=coterie_db
POSTGRES_USER=coterie_user
POSTGRES_PASSWORD=securepassword
DB_HOST=localhost  # Use 'db' if running inside Docker
DB_PORT=5432

# Django Configuration
DEBUG=True
SECRET_KEY=your_secret_key_here
ALLOWED_HOSTS=127.0.0.1,localhost

# Docker Environment Detection
IS_DOCKER=False  # Set to True when running inside Docker
```

Key Notes:
- Change passwords before deploying to production.
- `DB_HOST=localhost` for local development and `DB_HOST=db` for Docker.
- `IS_DOCKER=True` should be set inside Docker via `docker-compose.yml`.

---

## Running the Application

### Running Locally (Without Docker)
```sh
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Running with Docker
```sh
docker compose up --build -d
```
To stop:
```sh
docker compose down
```

---

## Creating a Superuser for Django Admin
After running the application, create an admin user manually:
```sh
docker compose exec web python manage.py createsuperuser
```
Use the credentials to log in at:
http://127.0.0.1:8000/admin/

---

## Troubleshooting
### Database Connection Issues
```sh
docker compose logs db | tail -n 20
```
Ensure that the correct `DB_HOST` is being used:
```sh
docker compose exec web python -c "import os; print(os.getenv('DB_HOST'))"
```

### Reset Docker & Database Volumes
If you need a fresh start:
```sh
docker compose down -v
```


