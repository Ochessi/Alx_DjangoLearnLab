from rest_framework import serializers
from .models import Author, Book
import datetime
from rest_framework.exceptions import ValidationError

class BookSerializer(serializers.ModelSerializer):
    """
    Serializes Book instances.
    - Validates publication_year to ensure it is not in the future.
    - Includes the author foreign key (as an id) so Book can be created/updated directly via the Book endpoint.
    """
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'publication_year']

    def validate_publication_year(self, value):
        current_year = datetime.datetime.now().year
        if value > current_year:
            raise ValidationError("Publication year cannot be in the future.")
        return value

class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializes Author instances.
    - includes nested BookSerializer for the related books (read-only).
    - This nested list is dynamic and will reflect current related Book objects.
    - To create books, use the Book endpoints in this simple approach.
    """
     
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']  