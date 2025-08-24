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



## Posts API

Base path: `/api/posts/`

Resources:
- `GET /api/posts/` — list posts (paginated). Query params: `page`, `page_size`, `search`, `author__username`, `ordering`.
- `POST /api/posts/` — create a post. Auth required.
  Body: `{ "title": "string", "content": "string" }`
- `GET /api/posts/{id}/` — retrieve a single post (includes nested comments).
- `PATCH /api/posts/{id}/` — update a post (author only).
- `DELETE /api/posts/{id}/` — delete a post (author only).

## Comments API

Base path: `/api/comments/`

- `GET /api/comments/` — list comments (paginated). Filter by `post`.
- `POST /api/comments/` — create comment. Body: `{ "post": post_id, "content": "text" }`
- `PATCH /api/comments/{id}/` — update comment (author only).
- `DELETE /api/comments/{id}/` — delete comment (author only).

