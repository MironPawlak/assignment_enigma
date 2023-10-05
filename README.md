## Getting Started
Project is configured to run on dockercompose up, and should migrate on start. To run the project, follow these steps:

1. Clone the repository: ``git clone https://github.com/MironPawlak/assignment_enigma.git``
2. Run the following command to build and start the containers:: ``docker-compose up --build``
3. Migrations will perform automatically

## Testing
To run test, use the following command
``docker exec -it <container_name> python3 manage.py test``
