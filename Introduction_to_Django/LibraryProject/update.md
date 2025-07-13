from bookshelf.models import Book

# Update the book title
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
print(book)
# Output: Nineteen Eighty-Four by George Orwell (1949)
