FROM python:3.12-slim


RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /django_app

COPY requirements.txt /django_app/registration_platform_front/requirements.txt

RUN pip install --no-cache-dir -r /django_app/registration_platform_front/requirements.txt

COPY . /django_app/registration_platform_front

WORKDIR /django_app/registration_platform_front

EXPOSE 8001

CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]