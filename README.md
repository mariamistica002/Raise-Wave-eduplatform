# RW EduPlatform – Full Stack

**Built by RW Software Development** · [rwsoftwaredevelopment.com](https://rwsoftwaredevelopment.com)

A production-ready educational platform with Django REST Framework backend, PostgreSQL database, Redis caching, WebSocket real-time notifications, and full API integration for the HTML frontend.

---

## Stack

| Layer      | Technology                              |
|------------|-----------------------------------------|
| Frontend   | HTML5 / CSS3 / Vanilla JS               |
| Backend    | Django 4.2 + Django REST Framework      |
| Database   | PostgreSQL 16                           |
| Cache      | Redis 7                                 |
| WebSocket  | Django Channels + Daphne                |
| Auth       | JWT (SimpleJWT)                         |
| Web Server | Nginx + Gunicorn                        |
| Container  | Docker + Docker Compose                 |

---

## Project Structure

```
rw-eduplatform/
├── backend/
│   ├── eduplatform/        # Django project settings, urls, asgi, wsgi
│   ├── users/              # Auth, registration, institutions, profiles
│   ├── courses/            # Courses, departments, topics, study materials
│   ├── attendance/         # Attendance sessions, bulk marking, reports
│   ├── tests/              # Exams, questions, choices, attempts, scoring
│   ├── fees/               # Fee categories, structures, payments
│   ├── notices/            # Announcements and notices
│   ├── api/                # Dashboard stats, WebSocket consumer
│   ├── manage.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── rw-eduplatform.html # Main landing page
│   └── api.js              # Frontend ↔ Backend API client
├── nginx/
│   └── nginx.conf
├── scripts/
│   └── seed.py             # Demo data seeder
├── docker-compose.yml
└── README.md
```

---

## Option A – Run with Docker (Recommended)

### Prerequisites
- Docker Desktop installed and running
- Git

### Steps

```bash
# 1. Clone / extract the project
cd rw-eduplatform

# 2. Build and start all services
docker compose up --build -d

# 3. Run database migrations (first time only)
docker compose exec backend python manage.py migrate

# 4. Create superuser (optional – seed.py also creates one)
docker compose exec backend python manage.py createsuperuser

# 5. Load demo data
docker compose exec backend python /scripts/seed.py
# OR copy seed.py into backend and run:
docker compose exec backend python seed.py

# 6. Open the platform
#    Frontend  →  http://localhost
#    API Docs  →  http://localhost/api/docs/
#    Admin     →  http://localhost/admin/
```

---

## Option B – Run Locally (Development)

### Prerequisites
- Python 3.12+
- PostgreSQL 14+
- Redis 7+

### Steps

```bash
# 1. Set up the database
psql -U postgres -c "CREATE DATABASE rw_eduplatform;"

# 2. Set up Python environment
cd backend
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your DB password, secret key, etc.

# 4. Run migrations
python manage.py migrate

# 5. Seed demo data
python ../scripts/seed.py

# 6. Start Django (HTTP)
python manage.py runserver 0.0.0.0:8000

# 7. Start Daphne (WebSocket) – in a second terminal
daphne -b 0.0.0.0 -p 8001 eduplatform.asgi:application

# 8. (Optional) Start Celery worker – in a third terminal
celery -A eduplatform worker -l info
```

Open `frontend/rw-eduplatform.html` directly in the browser or serve it with:
```bash
cd ../frontend && python -m http.server 3000
```

---

## API Endpoints Reference

### Auth
| Method | Endpoint                      | Description              |
|--------|-------------------------------|--------------------------|
| POST   | /api/v1/auth/login/           | Login → JWT tokens       |
| POST   | /api/v1/auth/register/        | Register new user        |
| POST   | /api/v1/auth/logout/          | Blacklist refresh token  |
| POST   | /api/v1/auth/token/refresh/   | Refresh access token     |
| GET    | /api/v1/auth/me/              | Current user profile     |
| POST   | /api/v1/auth/change-password/ | Change password          |
| POST   | /api/v1/auth/demo-request/    | Submit demo request      |

### Courses
| Method | Endpoint                         | Description           |
|--------|----------------------------------|-----------------------|
| GET    | /api/v1/courses/                 | List courses          |
| POST   | /api/v1/courses/                 | Create course         |
| GET    | /api/v1/courses/{id}/            | Course detail         |
| POST   | /api/v1/courses/{id}/enroll/     | Enroll student        |
| GET    | /api/v1/courses/{id}/materials/  | List study materials  |

### Attendance
| Method | Endpoint                               | Description           |
|--------|----------------------------------------|-----------------------|
| GET    | /api/v1/attendance/sessions/           | List sessions         |
| POST   | /api/v1/attendance/sessions/           | Create session        |
| POST   | /api/v1/attendance/bulk/               | Mark bulk attendance  |
| GET    | /api/v1/attendance/summary/            | My attendance %       |

### Exams
| Method | Endpoint                    | Description              |
|--------|-----------------------------|--------------------------|
| GET    | /api/v1/tests/              | List exams               |
| POST   | /api/v1/tests/{id}/start/   | Start exam attempt       |
| POST   | /api/v1/tests/submit/       | Submit exam answers      |
| GET    | /api/v1/tests/results/      | View results             |

### Fees
| Method | Endpoint                    | Description              |
|--------|-----------------------------|--------------------------|
| GET    | /api/v1/fees/payments/      | List payments            |
| POST   | /api/v1/fees/payments/      | Record payment           |
| GET    | /api/v1/fees/summary/       | Fee summary              |

### Dashboard & Notices
| GET | /api/v1/dashboard/     | Role-based stats     |
| GET | /api/v1/notices/       | Published notices    |

### WebSocket
```
ws://your-domain/ws/notifications/
```

---

## Frontend API Client Usage

Add `api.js` to any HTML page to interact with the backend:

```html
<script src="api.js"></script>
<script>
  // Login
  RW.AuthAPI.login('student1', 'Student@1234').then(data => {
    console.log('Logged in as:', data.user.first_name);
  });

  // Get dashboard stats
  RW.DashboardAPI.getStats().then(stats => {
    console.log(stats);
  });

  // Submit demo request from CTA (auto-wired to .cta-submit button)
  // Just include api.js – it handles the CTA form automatically.

  // Real-time notifications
  RW.RWSocketClient.connect();
  RW.RWSocketClient.on('notification', (data) => {
    RW.UI.showToast(data.message, 'info');
  });
</script>
```

---

## Default Login Credentials (after seeding)

| Role    | Username  | Password      |
|---------|-----------|---------------|
| Admin   | admin     | Admin@1234    |
| Teacher | teacher1  | Teacher@1234  |
| Student | student1  | Student@1234  |
| Student | student2  | Student@1234  |
| Student | student3  | Student@1234  |

---

## Production Deployment Checklist

- [ ] Set `DEBUG=False` in `.env`
- [ ] Generate a strong `SECRET_KEY` (50+ chars)
- [ ] Set `ALLOWED_HOSTS` to your actual domain
- [ ] Set `CORS_ALLOWED_ORIGINS` to your frontend domain
- [ ] Use a strong PostgreSQL password
- [ ] Enable HTTPS (SSL certificate via Let's Encrypt / Certbot)
- [ ] Set up automated PostgreSQL backups
- [ ] Configure email settings for notifications
- [ ] Run `python manage.py collectstatic`

---

## Support

Built by **RW Software Development**  
🌐 [rwsoftwaredevelopment.com](https://rwsoftwaredevelopment.com)
