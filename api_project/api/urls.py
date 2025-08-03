# api/urls.py

from django.urls import path, include
from rest_framework import routers
from .views import BookList, BookViewSet
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()
router.register(r'books_all', BookViewSet, basename='books_all')

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),
    path('api-token-auth/', obtain_auth_token, name='api-token-auth'),
    path('', include(router.urls)),
]