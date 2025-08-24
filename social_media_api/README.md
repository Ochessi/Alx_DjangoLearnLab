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




## Follow System
- `POST /api/accounts/follow/<user_id>/` → follow a user (auth required).
- `POST /api/accounts/unfollow/<user_id>/` → unfollow a user (auth required).

## Feed
- `GET /api/feed/` → returns posts from users the authenticated user follows.




## Likes
- `POST /api/posts/{id}/like/` — Like a post (auth required). Returns Like object.
- `POST /api/posts/{id}/unlike/` — Unlike a post (auth required).

## Notifications
- `GET /api/notifications/` — List current user's notifications (auth required).
- `PATCH /api/notifications/{id}/mark-read/` — Mark notification as read (auth required).

Notifications payload example:
{
  "id": 12,
  "recipient": "alice",
  "recipient_id": 3,
  "actor": "bob",
  "actor_id": 4,
  "verb": "liked your post",
  "target": 5,
  "target_repr": "My first post",
  "unread": true,
  "timestamp": "2025-08-24T12:00:00Z"
}


