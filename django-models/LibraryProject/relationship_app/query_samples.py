import os
import django

# Setup Django environment (only needed if running standalone)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# Query: All books by a specific author
def get_books_by_author(author_name):
    books = Book.objects.filter(author__name=author_name)
    print(f"Books by {author_name}: {[book.title for book in books]}")

# Query: List all books in a library
def list_books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        print(f"Books in {library_name}: {[book.title for book in books]}")
    except Library.DoesNotExist:
        print(f"No library named {library_name}")

# Query: Retrieve the librarian for a library
def get_librarian_for_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        librarian = Librarian.objects.get(library=library)
        print(f"Librarian of {library_name}: {librarian.name}")
    except (Library.DoesNotExist, Librarian.DoesNotExist):
        print(f"Librarian not found for library {library_name}")

# --- Sample Calls ---
# You can uncomment these to test after creating data via Django admin or shell

# get_books_by_author("Jane Austen")
# list_books_in_library("Central Library")
# get_librarian_for_library("Central Library")
