# test for task 1

```bash
python manage.py shell
```

```python
from api.models import Author, Book
from api.serializers import AuthorSerializer, BookSerializer
from datetime import date

# Create Author
a = Author.objects.create(name="J.K. Rowling")

# Create Book
b1 = Book.objects.create(title="Harry Potter and the Sorcerer's Stone", publication_year=1997, author=a)
b2 = Book.objects.create(title="Harry Potter and the Chamber of Secrets", publication_year=1998, author=a)

# Serialize author
serializer = AuthorSerializer(a)
print(serializer.data)
```