# Update a Book Record

This document explains how to update an existing `Book` record using the Django ORM.

## Retrieve the Book First

```python
from books.models import Book

book = Book.objects.get(title="1984")

book.title = "Nineteen Eighty-Four"
book.save()

Book.objects.get(id=book.id).title
```

## Output

'Nineteen Eighty-Four'
