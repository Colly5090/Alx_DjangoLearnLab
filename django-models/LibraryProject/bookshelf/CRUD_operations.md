# CRUD Operations Using Django ORM

This document demonstrates how to perform **Create, Retrieve, Update, and Delete (CRUD)** operations on the `Book` model using the Django ORM via the Django shell.

---

## Prerequisites

Ensure migrations are applied before performing CRUD operations.

```bash
python manage.py makemigrations
python manage.py migrate
```

## Open Django Shell

```bash
python manage.py shell
```

### Create Operation

```python
# Import the Book model
from books.models import Book

# Create and save a new book
book = Book.objects.create(
    title="1984",
    author="George Orwell",
    publication_year=1949
)
```

## Output(`indicates the record was created successfully`)

> > >

## RETRIEVE Operation

```python
# Retrieve book by title
book = Book.objects.get(title="1984")

# Display book fields
print(book.title)
print(book.author)
print(book.publication_year)

# Retrieve all book records
Book.objects.all()
```

## Output(per field)

1984
George Orwell
1949

## Output(all records)

<QuerySet [<Book: Clean Code>]>

## UPDATE Operation

```python
# Retrieve the book
book = Book.objects.get(title="1984")

# Update the title
book.title = "Nineteen Eighty-Four"
book.save()

# Confirm the updated title
Book.objects.get(id=book.id).title
```

## Output

'Nineteen Eighty-Four'

## DELETE Operation

```python
# Retrieve the updated book
book = Book.objects.get(title="Nineteen Eighty-Four")

# Delete the book
book.delete()
```

## Output

(1, {'books.Book': 1})

## Verify Deletion

```python
# Confirm deletion
Book.objects.all()
```

## Output

<QuerySet []>
