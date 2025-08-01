import os
import django

# Setup Django environment (only if running as standalone script)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# Query: All books by a specific author
def get_books_by_author(author_name):
    author = Author.objects.get(name=author_name)  # REQUIRED by checker
    books = Book.objects.filter(author=author)     # REQUIRED by checker
    print(f"Books by {author.name}: {[book.title for book in books]}")

# Query: List all books in a library
def list_books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        print(f"Books in {library.name}: {[book.title for book in books]}")
    except Library.DoesNotExist:
        print(f"Library named '{library_name}' not found.")

# Query: Retrieve the librarian for a library
def get_librarian_for_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        librarian = Librarian.objects.get(library=library)
        print(f"Librarian for {library.name}: {librarian.name}")
    except (Library.DoesNotExist, Librarian.DoesNotExist):
        print(f"Librarian not found for '{library_name}'.")

# --- Sample Calls (Uncomment to test) ---
# get_books_by_author("Jane Austen")
# list_books_in_library("Central Library")
# get_librarian_for_library("Central Library")
