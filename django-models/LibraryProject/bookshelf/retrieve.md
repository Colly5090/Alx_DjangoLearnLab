# Retrieve a Book Record

This document shows how to retrieve existing `Book` records from the database using Django ORM.

## Retrieve a Single Book by Title

```python
from books.models import Book

book = Book.objects.get(title="1984")
```

## Display Retrieved Data

```python
print(book.title)
print(book.author)
print(book.publication_year)
```

## Output

1984
George Orwell
1949

## Retrieve All Books

```python
Book.objects.all()
```

## Output

<QuerySet [<Book: Clean Code>]>
