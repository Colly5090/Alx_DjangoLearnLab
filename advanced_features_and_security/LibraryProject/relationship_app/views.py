from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, CreateView, TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import user_passes_test, permission_required
from django.contrib.auth import logout
from django.urls import reverse_lazy, reverse
from .models import Book, Library, UserProfile
from .forms import BookForm

def list_books(request):
    books = Book.objects.select_related('author').all()
    return render(request, 'relationship_app/list_book.html', {'books': books})

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'relationship_app/register.html'
    success_url = reverse_lazy('login')

class UserLoginView(LoginView):
    template_name = 'relationship_app/login.html'

    def get_success_url(self):
        role = self.request.user.userprofile.role
        if role == 'Admin':
            return reverse('admin_view')
        elif role == 'Librarian':
            return reverse('librarian_view')
        return reverse('member_view')

class UserLogoutView(TemplateView):
    template_name = 'relationship_app/logout.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        return render(request, self.template_name)
    
def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

# Admin view
@user_passes_test(is_admin)
def admin_view(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/admin_view.html', {'books': books})

# Librarian view
@user_passes_test(is_librarian)
def librarian_view(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/librarian_view.html', {'books': books})

# Member view
@user_passes_test(is_member)
def member_view(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/member_view.html', {'books': books})


@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(redirect_by_role(request.user))
    else:
        form = BookForm()
    return render(request, 'relationship_app/book_form.html', {'form': form, 'action': 'Add', 'cancel_url': redirect_by_role(request.user)})
    
@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect(redirect_by_role(request.user))
    else:
        form = BookForm(instance=book)
    return render(request, 'relationship_app/book_form.html', {'form': form, 'action': 'Edit', 'cancel_url': redirect_by_role(request.user)})

@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect(redirect_by_role(request.user))
    return render(request, 'relationship_app/book_confirm_delete.html', {'book': book, 'cancel_url':  redirect_by_role(request.user)})


def redirect_by_role(user):
    role = user.userprofile.role
    if role == 'Admin':
        return reverse('admin_view')
    elif role == 'Librarian':
        return reverse('librarian_view')
    else:
        return reverse('member_view')