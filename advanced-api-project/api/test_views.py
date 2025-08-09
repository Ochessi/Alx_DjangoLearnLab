"""
Tests for the Book API endpoints.

Covers:
- List (with filtering/search/ordering)
- Retrieve
- Create (authenticated only)
- Update (authenticated only)
- Delete (authenticated only)
- Permission enforcement (IsAuthenticated / IsAuthenticatedOrReadOnly)

This file uses DRF's APITestCase which gives us an APIClient and a fresh test DB.
"""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Book, Author
from django.contrib.auth.models import User

class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='pass123')
        self.author = Author.objects.create(name="John Doe")
        self.book = Book.objects.create(
            title="Python Basics", author=self.author, publication_year=2020
        )

        self.list_url = reverse('book-list')
        self.detail_url = reverse('book-detail', kwargs={'pk': self.book.pk})

    def test_list_books(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_book_authenticated(self):
        self.client.login(username='testuser', password='pass123')
        data = {
            "title": "New Book",
            "author": self.author.id,
            "publication_year": 2021
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_create_book_unauthenticated(self):
        data = {
            "title": "Unauthorized Book",
            "author": self.author.id,
            "publication_year": 2021
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book(self):
        self.client.login(username='testuser', password='pass123')
        data = {"title": "Updated Title", "author": self.author.id, "publication_year": 2020}
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Title")

    def test_delete_book(self):
        self.client.login(username='testuser', password='pass123')
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_filter_books_by_title(self):
        response = self.client.get(self.list_url, {'title': 'Python Basics'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_books(self):
        response = self.client.get(self.list_url, {'search': 'Python'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_order_books_by_year(self):
        Author.objects.create(name="Jane Smith")
        Book.objects.create(title="Older Book", author=self.author, publication_year=2010)
        response = self.client.get(self.list_url, {'ordering': 'publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            response.data[0]['publication_year'] <= response.data[1]['publication_year']
        )
