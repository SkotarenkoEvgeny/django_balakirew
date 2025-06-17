# Sitewomen

**Sitewomen** is an educational project designed for advanced learning of the Django framework. It serves as a practical platform to explore Django architecture, user management, media handling, and social authentication.

---

## 🔍 Project Highlights

- Multi-app Django project structure
- Custom user management and authentication
- Social login via OAuth (Google, etc.)
- Media file support (photos, uploads)
- Custom template filters and tags (`templatetags`)
- Custom context processors
- Captcha-protected forms
- Modular and scalable codebase

---

## 🛠 Technologies Used

- **Python** 3.x
- **Django** 4.2.x
- **Pillow** – image processing
- **django-simple-captcha** – CAPTCHA in forms
- **python-social-auth**, **social-auth-app-django** – OAuth login
- **django-ranged-response** – range-based media streaming
- And more (see `requirements.txt`)

---

## 📂 Project Structure

```text
sitewomen/
├── manage.py
├── db.sqlite3
├── requirements.txt
├── media/
│   ├── photos/
│   ├── uploads_model/
│   └── users/
├── templates/
│   └── base.html
├── sitewomen/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── users/
│   ├── forms.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── authentication.py
│   ├── context_processors.py
│   └── ...
└── women/
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── admin.py
    ├── fixtures/
    ├── static/
    ├── templates/
    ├── templatetags/
    ├── site_maps.py
    ├── utils.py
    └── ...



---

## 🚀 Getting Started

```bash
# Clone the repository
git clone https://github.com/your-username/sitewomen.git
cd sitewomen

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# (Optional) Create a superuser
python manage.py createsuperuser

# Run the development server
python manage.py runserver

## ✅ TODO

Here's a list of planned features and improvements:

- 🧪 Add unit and integration tests for critical components
- 🐳 Dockerize the application (Docker + docker-compose)
- 🌐 Implement internationalization (i18n) for multi-language support
- 🔐 Add permission-based access control for user roles
- 📦 Create seed data using fixtures for development
- 🧩 Refactor templates into reusable components (partials)
- 📊 Add admin dashboard with stats and analytics
- ☁️ Prepare for deployment (Heroku, Render, or custom VPS)
- 🔁 Setup CI/CD pipeline (GitHub Actions or similar)
- 📝 Improve documentation (usage, deployment, API)

