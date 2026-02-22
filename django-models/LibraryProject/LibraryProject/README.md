# LibraryProject

LibraryProject is a simple Django-based web application created to demonstrate core Django concepts such as project setup, ORM usage, Django Admin, and CRUD operations. This project serves as a solid foundation for building scalable backend systems and REST APIs.

---

## 🚀 Features

- Clean Django project and app structure
- Database interaction using Django ORM
- Full CRUD operations via Django shell and Admin
- Customizable Django Admin interface
- Ready for Django REST Framework integration
- Beginner-friendly and production-aligned setup

---

## 🛠️ Tech Stack

- **Python 3**
- **Django**
- **SQLite** (default database)

---

## 📦 Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Colly5090/Alx_DjangoLearnLab.git
cd LibraryProject

### 2️⃣ Start a New Project
django-admin startproject LibraryProject
cd LibraryProject
```

### 3️⃣ Create an App

python manage.py startapp bookshelf

## ⚙️ Register App in Django Settings

### 4️⃣ Add `bookshelf` App to INSTALLED_APPS at `LibraryProject/settings.py`

## 🧱 Create the Book Model

### 5️⃣ Edit `books/models.py`

## 🗄️ Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## 🧪 Perform CRUD Using Django Shell

```bash
python manage.py shell
```

Follow the cheatsheet below:

# CREATE

Book.objects.create(...)

# READ

Book.objects.get(...)
Book.objects.all()

# UPDATE

book.field = value
book.save()

# DELETE

book.delete()

## 🔐 Django Admin Setup

```bash
python manage.py createsuperuser
```

### Register Book Model in Admin in `bookshelf/admin.py`

### 🎛️ Customize the Admin Interface

Add list view for (Title, Author, Publication_year)
Search field
Filtering

## ▶️ Run the Development Server

```bash
python manage.py runserver
```

Access the Admin panel:
http://127.0.0.1:8000/admin/
