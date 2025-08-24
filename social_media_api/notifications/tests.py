from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Post, Like

User = get_user_model()

class LikeNotificationTest(APITestCase):
    def setUp(self):
        self.a = User.objects.create_user('a','a@example.com','pass')
        self.b = User.objects.create_user('b','b@example.com','pass')
        self.post = Post.objects.create(author=self.a, title='t', content='c')

    def test_like_creates_notification(self):
        self.client.force_authenticate(user=self.b)
        resp = self.client.post(reverse('post-like', args=[self.post.id]))  # name depends on router; often 'post-like'
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(Like.objects.filter(user=self.b, post=self.post).exists())
        # Check notification exists for post author
        from notifications.models import Notification
        self.assertTrue(Notification.objects.filter(recipient=self.a, actor=self.b, verb__icontains='liked').exists())
