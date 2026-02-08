from django.db import models

class Author(models.Model):
    """
    Represents an author of books.

    Fields:
    - name: the name of the author
    - books: a one-to-many relationship to Book model
    """
    name = models.CharField(max_length=255)

class Book(models.Model):
    """
    Represents a book written by an author.

    Fields:
    - title: the title of the book
    - publication_year: the year the book was published
    - author: foreign key to the Author model
    - related_name 'books' allows reverse access from Author to their books
    """
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
