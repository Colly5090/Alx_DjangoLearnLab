import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Book, Librarian, Library, Author

def sample_queries():
    # 1. Query all books by a specific author
    author_name = "John Doe"
    books_by_author = Book.objects.filter(author__name=author_name)
    print(f"Books by {author_name}: {[book.title for book in books_by_author]}")

    # 2. List all books in a library
    library_name = "Central Library"
    try:
        library = Library.objects.get(name=library_name)
        books_in_library = library.books.all()
        print(f"Books in {library_name}: {[book.title for book in books_in_library]}")
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")

    # 3. Retrieve the librarian for a library
    try:
        librarian = Librarian.objects.get(library__name=library_name)
        print(f"Librarian for {library_name}: {librarian.name}")
    except Librarian.DoesNotExist:
        print(f"No librarian assigned for '{library_name}'.")


if __name__ == "__main__":
    sample_queries()