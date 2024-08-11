# Test Acreditta

## Installation

### Local Installation

1. Create a virtual environment using:`python -m venv venv`'
2. Activate the virtual environment using: `.\venv\Scripts\activate` or `source venv/bin/activate`
3. Install the requirements using: `pip install -r requirements.txt`
4. Create a `.env` file in the root directory and add the below content: Use `.env-example` as a reference
5. Run the migrations using: `python manage.py migrate`
6. Run the server using: `python manage.py runserver`
7. Access the API using the URL: `http://localhost:8000/api/docs`

### Docker Installation

1. Create a `.env` file in the root directory and add the below content: Use `.env-example` as a reference
2. Run the docker-compose file using: `docker-compose up -d` or use make command `make run`

## API Endpoints and Description

visit the URL: `https://gorgeous-abigail-jhon-acevedo-89f0a988.koyeb.app/` to access the API documentation or use the
below information:

This project contains the code for creating the below four apis:

| API Endpoint          | Method | Description                                       | Authorization Required | Request Body                                                                                                 |
|-----------------------|--------|---------------------------------------------------|------------------------|--------------------------------------------------------------------------------------------------------------|
| /api/login/           | POST   | Obtain credentials for endpoints with Bearer Auth | No                     | {"email": "user@example.com", password:"password"}                                                           |
| api/create_user/      | POST   | Create a new user                                 | No                     | {"email": "user@example.com", "password": "Password.1","name": "name"}                                       |
| /api/badge            | GET    | Get list of badges                                | Yes                    | No                                                                                                           |
| /api/badge            | POST   | Create a new badge                                | Yes                    | {"name": "Badge Name", "description": "Badge Description", "image": "optional_imagen_file or upload image" } |
| /api/badge/{badge_id} | GET    | Get a badge by UUID                               | Yes                    | NO                                                                                                           |

