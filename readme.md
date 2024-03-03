# Pokemon API

## Requirements to Run the Application
- Docker and docker compose installed on your system

## Steps to Run the Application
1. Clone this repository to your local machine.
2. Navigate to the root directory of the project.
3. Create a `.env` file in the root directory of the project and add the following SECRET_KEY="your_secret_key"
4. Build and run the Docker image using the provided Dockerfile:
    1. docker-compose build
    2. docker-compose up
5. Access the API at http://localhost:5000.


## Description of Routes

### Authentication Routes
- `/auth/register` (POST): Registers a new user. Requires a JSON body with "email" and "password" fields. obs: 'Password must have at least 8 characters, one uppercase letter, one lowercase letter, and one digit."
- `/auth/login` (POST): Logs in a user. Requires a JSON body with "email" and "password" fields.
- `/auth/logout` (POST): Logs out the currently logged-in user.

### Pokemon Routes (Protected)
These routes require authentication and can only be accessed after logging in.

- `/app/pokemon/<name>` (GET): Retrieves the types of a Pokemon by its name.
- `/app/pokemon/type/<type>` (GET): Retrieves a random Pokemon by its type.
- `/app/pokemon/long/<type>` (GET): Retrieves the Pokemon with the longest name by its type.
- `/app/pokemon/iam` (GET): Retrieves a random Pokemon based on the current weather.