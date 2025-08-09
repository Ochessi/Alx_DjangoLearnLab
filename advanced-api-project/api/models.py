from django.db import models

class Author(models.Model):
    """
    Author model:
    - Stores an author's name.
    - One-to-many relation: an Author can have many Book objects.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Book model:
    - title: the book's title (string)
    - publication_year: integer year the book was published
    - author: ForeignKey to Author establishing Author -> Books relationship.
      related_name='books' allows Author.books.all() to access related books.
    """
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
