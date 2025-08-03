"""
Authentication & Permissions Setup:

- Uses DRF's TokenAuthentication.
- Each user must obtain a token via POST to /api-token-auth/ with username and password.
- All API endpoints are protected with IsAuthenticated by default.
- To access protected endpoints, include the token in the Authorization header:
  Authorization: Token <your_token_here>
"""


from rest_framework import generics, viewsets, permissions
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]    