# Image hosting API - Florina Biletsiou

Solution for the Backend Code Test for Disco .


## Getting Started


### Prerequisites

Requirements for the software and other tools to build, test and push 
- [Python 3](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Docker](https://docs.docker.com/get-docker/)
- [Postgres](https://www.postgresql.org/)
- [Pytest](https://docs.pytest.org/)


### Docker - Database install
[Install Docker](https://docs.docker.com/get-docker/) for your system and ensure that the Docker daemon is running.
Then build the docker image and run it:

    sudo docker build . -f Dockerfile --network=host
    sudo docker-compose up -d --build

I developed the code in a Windows operating system, where the docker installation was smooth. 
Nonetheless, when using Linux-type operating systems there were a few issues coming from the system itself that needed additional steps.

I can't include all the possible issues here, but the commands below seemed to be helpful for the most common issues.
Troubleshooting:
    
    docker-compose down
    docker-compose up --force-recreate
    (port already in use) sudo service postgresql stop


#### Running the database locally

download a compatible [PostgreSQL installer](https://www.postgresql.org/download/windows/) from the official website of PostgreSQL (for windows).
Log into an interactive Postgres session either by the terminal or pgadmin4 and run:

```postgresql
CREATE DATABASE image_hosting_db;
CREATE USER django_user WITH PASSWORD 'postgres';

ALTER ROLE django_user SET client_encoding TO 'utf8';
ALTER ROLE django_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE django_user SET timezone TO 'UTC';

ALTER USER django_user CREATEDB;
GRANT ALL ON SCHEMA public TO django_user;
GRANT ALL PRIVILEGES ON DATABASE image_hosting_db TO django_user;

```

To run the database locally, go to `core/settings` and use the database option:

    # FOR LOCAL USE
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            ...
            ...


### Running the project

After installing the prerequisites mentioned above, follow the steps below to run the application locally.

Create and activate the project's virtual environment:

    [Locally]
    python -m venv env
    source env/bin/activate

Install the project dependencies:
    
    [Locally]
    python -m pip install -r requirements.txt

Apply any available migrations:
    
    [Locally]
    python manage.py makemigrations
    python manage.py migrate
    [Docker]
    docker-compose exec web python manage.py migrate

Running the server (from the `./app` location):

    [Locally]
    python manage.py runserver

Now the app should be successfully running and ready to use.

## Authorization and User accounts

Most API calls require the user to be authenticated in order to access the results.

For this project I've implemented the token authentication method that the Django REST framework provides.

The easiest way to create a superuser account is with the command:

    [Locally]
    python manage.py createsuperuser
    [Docker]    
    docker-compose exec web python manage.py createsuperuser

When it comes to the **creation of simple User accounts (for this occasion) is through the admin panel**. 

Last, to get a token for a user use the command:

    [Locally]
    python manage.py drf_create_token <username>
    [Docker]
    docker-compose exec web python manage.py drf_create_token <username>

This token should be included to the HTTP request's headers as:

    {"Authorization": "Token <token value>"}

Alternatively, there is the option of using the Browsable Rest API too.


#### IMPORTANT

When you're done, close down your Docker container since it can consume a lot of computer memory.

    docker-compose down


## Tests

To run the tests type from the base directory:

    pytest

## Authors

  - [Florina Biletsiou](https://www.linkedin.com/in/florina-biletsiou/)
