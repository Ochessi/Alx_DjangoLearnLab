# Social Media API (Django + DRF)

## Quick start

1. Create venv & install:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

2. Ensure AUTH_USER_MODEL = 'accounts.User' is set in settings.py.

3. Run migrations:

   python manage.py makemigrations
   python manage.py migrate

4. Create superuser:
    python manage.py createsuperuser

5. Run server:
     python manage.py runserver

Endpoints

POST /api/accounts/register/ — register new user; returns { token, user }

POST /api/accounts/login/ — login; returns { token, user }

GET/PATCH /api/accounts/profile/ — get/update authenticated user

GET /api/accounts/profile/<username>/ — public profile
