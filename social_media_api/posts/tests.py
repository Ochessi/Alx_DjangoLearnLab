from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Post, Comment

User = get_user_model()

class PostCommentTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='alice', password='password123')
        self.other = User.objects.create_user(username='bob', password='password123')
        self.post = Post.objects.create(author=self.user, title='Hello', content='World')

    def test_create_post_requires_auth(self):
        url = reverse('post-list')  # router name: post-list
        data = {'title': 'New', 'content': 'Content'}
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.login(username='alice', password='password123')
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)

    def test_comment_creation_and_permissions(self):
        url = reverse('comment-list')
        self.client.login(username='bob', password='password123')
        data = {'post': self.post.id, 'content': 'Nice post!'}
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        comment_id = resp.data['id']

        # bob cannot update alice's post comment? he is author of comment so can update
        resp = self.client.patch(reverse('comment-detail', args=[comment_id]), {'content': 'Updated'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
