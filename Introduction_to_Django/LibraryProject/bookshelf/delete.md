# Delete a Book Record

This document demonstrates how to delete a `Book` record using the Django ORM.

## Retrieve the Book

```python
from bookshelf.models import Book

book = Book.objects.get(title="Nineteen Eighty-Four")

book.delete()
```

## Output

(1, {'books.Book': 1})

## Verify Deletion

```python
Book.objects.all()
```

## Output

<QuerySet []>
