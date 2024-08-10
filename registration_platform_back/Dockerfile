FROM python:3.12-slim


RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /django_app

COPY requirements.txt /django_app/registration_platform_back/requirements.txt

RUN pip install --no-cache-dir -r /django_app/registration_platform_back/requirements.txt

COPY . /django_app/registration_platform_back

WORKDIR /django_app/registration_platform_back

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]