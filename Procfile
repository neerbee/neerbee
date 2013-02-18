#web: django-admin.py runserver 0.0.0.0:$PORT --noreload
web: python manage.py collectstatic --noinput; gunicorn neerbee.wsgi
