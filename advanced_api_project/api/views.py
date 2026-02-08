from rest_framework import generics, permissions, filters
from .serializers import BookSerializer
from .models import Book
from django_filters.rest_framework import DjangoFilterBackend


# -------------------------------
# List all books
# -------------------------------

class BookListView(generics.ListAPIView):
    """
    GET /books/ - List all books
    open to all users (no authentication required)
    Query Parameters:
    - Filter: ?title=Harry Potter&author=1&publication_year=2007
    - Search: ?search=Rowling
    - Ordering: ?ordering=title,-publication_year
    """

    permission_classes = [permissions.AllowAny]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title', 'author', 'publication_year']
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']


# -------------------------------
# Retrieve a single book by ID
# -------------------------------
class BookDetailView(generics.RetrieveAPIView):
    """
    GET /books/<int:id>/ - Retrieve a single book by ID
    open to all users (no authentication required)
    """

    permission_classes = [permissions.AllowAny]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# -------------------------------
# Create a new book
# -------------------------------

class BookCreateView(generics.CreateAPIView):
    """
    POST /books/ - Create a new book
    requires authentication (only authenticated users can create books)
    """

    permission_classes = [permissions.IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# -------------------------------
# Update an existing book
# -------------------------------
class BookUpdateView(generics.UpdateAPIView):
    """
    PUT/ PATCH /books/<int:id>/ - Update an existing book
    requires authentication (only authenticated users can update books)
    """

    permission_classes = [permissions.IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# -------------------------------
# Delete a book
# -------------------------------
class BookDeleteView(generics.DestroyAPIView):
    """
    DELETE /books/<int:id>/ - Delete a book
    requires authentication (only authenticated users can delete books)
    """

    permission_classes = [permissions.IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer