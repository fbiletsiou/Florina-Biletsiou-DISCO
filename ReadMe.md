# Image hosting API - Florina Biletsiou

Solution for the Backend Code Test for Disco .


## Getting Started


### Prerequisites

Requirements for the software and other tools to build, test and push 
- [Python 3](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Pytest](https://docs.pytest.org/)

### Running the project

After installing the prerequisites mentioned above, follow the steps below to run the application locally.

Create and activate the project's virtual environment:

    python -m venv env
    source env/bin/activate

Install the project dependencies:

    python -m pip install -r requirements.txt

Apply any available migrations:
    
    python manage.py makemigrations
    python manage.py migrate

Running the server (from the `./app` location):

    python manage.py runserver

Now the app should be successfully running and ready to use.

## Authorization and User accounts

Most API calls require the user to be authenticated in order to access the results.

For this project I've implemented the token authentication method that the Django REST framework provides.

The easiest way to create a superuser account is with the command:

    python manage.py createsuperuser

When it comes to the **creation of simple User accounts (for this occasion) is through the admin panel**. 

Last, to get a token for a user use the command:

    python manage.py drf_create_token <username>

This token should be included to the HTTP request's headers as:

    {"Authorization": "Token <token value>"}

Alternatively, there is the option of using the Browsable Rest API too.

## Tests

Unfortunately, I decided to not include my progress when it comes to the testing because the code stated breaking and I didn't want to be more delayed. 
I am still working on them so there is a possibility that I will have updated this part. 


## Authors

  - [Florina Biletsiou](https://www.linkedin.com/in/florina-biletsiou/)
