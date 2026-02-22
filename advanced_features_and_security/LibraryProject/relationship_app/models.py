from django.db import models
from django.contrib.auth.models import User, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        permissions = [
            ("can_add_book", "Can add book"),
            ("can_change_book", "Can change book"),
            ("can_delete_book", "Can delete book"),
        ]

    def __str__(self):
        return self.title

class Library(models.Model):
    name = models.CharField(max_length=255)
    books = models.ManyToManyField(Book, related_name="libraries")

    def __str__(self):
        return self.name

class Librarian(models.Model):
    name = models.CharField(max_length=255)
    library = models.OneToOneField(Library, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username}"

# Helper function to assign role-based permissions
def assign_role_permissions(user, role):
    content_type = ContentType.objects.get_for_model(Book)

    if role == 'Member':
        perms = ['can_add_book', 'can_change_book']
    elif role == 'Librarian':
        perms = ['can_add_book', 'can_change_book']
    elif role == 'Admin':
        perms = ['can_add_book', 'can_change_book', 'can_delete_book']
    else:
        perms = []

    # Clear any existing permissions first
    user.user_permissions.clear()

    # Assign permissions to the user
    for perm_codename in perms:
        perm = Permission.objects.get(codename=perm_codename, content_type=content_type)
        user.user_permissions.add(perm)
    user.save()

# Signal to create UserProfile and assign default permissions
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile.objects.create(user=instance, role='Member')
        assign_role_permissions(instance, profile.role)

# Optional: Update permissions if role is changed
@receiver(post_save, sender=UserProfile)
def update_user_permissions(sender, instance, **kwargs):
    assign_role_permissions(instance.user, instance.role)

