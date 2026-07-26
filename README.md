# Scholarship Exam Management System

Full-stack web app built with **Django + MySQL** (backend) and **HTML/CSS/JS** (frontend, English UI).

## Features implemented

- **Role-based accounts** (`accounts` app): Student / Ambassador / Staff / Admin — one custom `User` model, each role redirected to its own dashboard after login.
- **Student dashboard** (`students` app): register for an exam, see payment status (paid/due), view/download admit card, edit profile.
- **Ambassador dashboard** (`ambassadors` app): unique referral code, list of students they referred, total registrations, total money collected, total due.
- **Admin panel** (`adminpanel` app):
  - `admin_dashboard` (ADMIN role): total forms sold, total paid, total due, per-ambassador collection report, exam list.
  - `staff_dashboard` (STAFF role): secure but **limited** view — student list, registrations, support inbox — financial totals hidden.
- **Support messaging** (`messaging` app): students send messages from the site, staff/admin see an inbox and reply.
- **Auto Admit Card generation** (`admitcard` app): a management command (`send_admit_cards`) generates a PDF admit card with `reportlab` and emails it automatically to students whose exam is `ADMIT_CARD_SEND_DAYS_BEFORE` days away (default 7) **and** whose payment is fully paid. Run it daily via cron:
  ```
  0 8 * * * /path/to/venv/bin/python manage.py send_admit_cards
  ```
- **Payments** (`payments` app): tracks `total_fee`, `amount_paid`, auto-computed `due_amount`, and status (Pending/Partial/Paid).
- **Exams** (`exams` app): exam name, date, time, venue, fee, deadline.

## Project structure

```
scholarship_project/
├── manage.py
├── requirements.txt
├── scholarship_project/      # settings, urls, wsgi, asgi
├── accounts/                 # custom User model, login/register, role decorator
├── students/                 # StudentProfile, ExamRegistration
├── ambassadors/               # AmbassadorProfile, referral logic
├── payments/                  # Payment model
├── exams/                     # Exam model
├── admitcard/                 # AdmitCard model + PDF/email auto-send
├── messaging/                  # SupportMessage
├── templates/                  # all HTML files (base.html has the navbar)
│   ├── base.html
│   ├── accounts/
│   ├── students/
│   ├── ambassadors/
│   ├── adminpanel/
│   ├── messaging/
│   └── exams/
└── static/
    ├── css/style.css
    └── js/script.js
```

## Setup

1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Create the MySQL database:
   ```sql
   CREATE DATABASE scholarship_db CHARACTER SET utf8mb4;
   ```

3. Set environment variables (or edit `settings.py` directly for local dev):
   ```bash
   export DB_NAME=scholarship_db
   export DB_USER=root
   export DB_PASSWORD=yourpassword
   export DB_HOST=localhost
   export DB_PORT=3306
   ```

4. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create a superuser (this becomes your ADMIN — after creating, set `role='ADMIN'` for this user in Django admin or shell):
   ```bash
   python manage.py createsuperuser
   python manage.py shell
   >>> from accounts.models import User
   >>> u = User.objects.get(username='youradminusername')
   >>> u.role = 'ADMIN'
   >>> u.save()
   ```

6. Run the dev server:
   ```bash
   python manage.py runserver
   ```

7. To create Ambassador and Staff accounts, log into `/django-admin/` (superuser) and either:
   - create a `User` there with `role='AMBASSADOR'`, then create a matching `AmbassadorProfile`, or
   - create a `User` there with `role='STAFF'`.

## Notes / Next steps for production

- Set `DEBUG = False`, a strong `SECRET_KEY`, and real `ALLOWED_HOSTS` before deploying.
- Switch `EMAIL_BACKEND` to a real SMTP backend (Gmail/SendGrid) and fill in `EMAIL_HOST_USER` / `EMAIL_HOST_PASSWORD`.
- For SMS-based admit card delivery instead of/along with email, plug your SMS gateway (e.g. a local BD SMS API or Twilio) into `admitcard/utils.py`.
- Schedule `send_admit_cards` via cron (Linux) or Task Scheduler (Windows), or wire it into Celery beat for a fully automatic setup.
- Add payment gateway integration (bKash/Nagad/SSLCommerz) to auto-update `Payment.amount_paid` instead of manual entry via Django admin.
