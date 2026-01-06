# Create a Book Record

This document demonstrates how to create a new `Book` record using the Django ORM from the Django shell.

## Command Used

### Openinig django Shell

```bash
python manage.py shell
```

### Create a `Book` instance

```python
from bookshelf.models import Book

book = Book.objects.create(
    title="1984",
    author="George Orwell",
    publication_year=1949
)
```

### Confirm created `Book` instance

```python
print(book)
```

### Output

1984 by George Orwell
