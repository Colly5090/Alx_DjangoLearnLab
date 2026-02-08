from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Author, Book
from django.contrib.auth import get_user_model

User = get_user_model()

class BookAPITestCase(APITestCase):
    """
    Unit tests for Book API endpoints including:
    - CRUD operations
    - Filtering, searching, ordering
    - Permission checks
    """

    def setUp(self):
        # Create a test user for authenticated operations
        self.user = User.objects.create_user(username="testuser", email="testuser@example.com", password="strongpass")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Create an author
        self.author = Author.objects.create(name="J.K Rowling")

        # Create sample books
        self.book1 = Book.objects.create(
            title="Harry Potter and the Philosopher's Stone",
            publication_year=1997,
            author=self.author
        )
        self.book2 = Book.objects.create(
            title="Harry Potter and the Chamber of Secrets",
            publication_year=1998,
            author=self.author
        )

    def test_list_books(self):
        """Test listing all books"""
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertIn('title', response.data[0])

    def test_create_book(self):
        """Test creating a new book"""
        url = reverse('book-create')
        data = {
            "title": "Harry Potter and the Prisoner of Azkaban",
            "publication_year": 1999,
            "author": self.author.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(response.data['title'], data['title'])

    def test_update_book(self):
        """Test updating an existing book"""
        url = reverse('book-update', kwargs={'pk': self.book1.id})
        data = {"title": "HP and the Sorcerer's Stone"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, data['title'])

    def test_delete_book(self):
        """Test deleting a book"""
        url = reverse('book-delete', kwargs={'pk': self.book2.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book2.id).exists())

    def test_filter_books_by_title(self):
        """Test filtering books by title"""
        url = reverse('book-list') + f"?title=Harry Potter and the Philosopher's Stone"
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.book1.title)

    def test_search_books(self):
        """Test searching books by author name"""
        url = reverse('book-list') + "?search=Rowling"
        response = self.client.get(url)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['author'], self.author.id)

    def test_order_books_by_publication_year(self):
        """Test ordering books descending by publication year"""
        url = reverse('book-list') + "?ordering=-publication_year"
        response = self.client.get(url)
        self.assertEqual(response.data[0]['publication_year'], 1998)

    def test_unauthenticated_create_forbidden(self):
        """Ensure unauthenticated users cannot create books"""
        client = APIClient()  # Unauthenticated client
        url = reverse('book-create')
        data = {"title": "Unauthorized Book", "publication_year": 2020, "author": self.author.id}
        response = client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

