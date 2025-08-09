from rest_framework import serializers
from .models import Author, Book
import datetime

class BookSerializer(serializers.ModelSerializer):
    """
    Serializes Book objects.
    - Validates that publication_year is not in the future.
    - When used top-level, 'author' will be the author's id.
    """
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    def validate_publication_year(self, value):
        """Ensure publication year is not greater than current year."""
        current_year = datetime.date.today().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializes Author objects.
    - Includes a nested list of BookSerializer results (read-only).
    - The nested field uses the Book model's related_name 'books' to pull related Book objects.
    """
    books = BookSerializer(many=True, read_only=True)  # read-only nested representation

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
