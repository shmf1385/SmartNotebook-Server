# How to run

##  Linux
```bash
    git clone https://github.com/SHMF1385/SmartNotebook-Server.git && cd SmartNotebook-Server
    virtualenv venv && source venv/bin/activate
    pip install -r requirements.txt
    mv core/settings.py.sample core/settings.py
```
Then edit core/settings.py

```python
    INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'notes',
    'users',
]
```

```python
    TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, '<your_templates_path>')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

```python
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.<your_database_engine',
        'HOST': '<db_host>',
        'NAME': '<db_name>',
        'USER': '<db_user>',
        'PASSWORD': '<db_password>',
        'PORT': '<db_port>'
    }
}
```

```python
    SENDER_EMAIL = "<sender_email_address>"
    SENDER_EMAIL_PASSWORD = "<sender_email_password>"
    STATIC_URL = "<static url>"
    STATICFILES_DIRS = (os.path.join(BASE_DIR, '<your_static_path>'),)
    STATIC_ROOT = '<path_for_django_statics>'
```