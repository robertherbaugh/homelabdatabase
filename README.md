# HomeLab Database

Welcome to HomeLab Database, a web application designed to help you organize and manage your home network infrastructure. This project represents my first foray into creating a Dockerized application, as well as my initial exploration into Continuous Integration and Continuous Deployment (CI/CD) practices. Built with Django and MySQL, this application serves as a central repository to keep track of Networks, Servers, Services, and Credentials securely.

## Key Features

- **Framework & Database**: Utilizes Django for the web framework and MySQL for data persistence.
- **Reverse Proxy Compatibility**: Tested and works seamlessly with Nginx as a reverse proxy.
- **Data Organization**: Easily manage details of your networks, servers, services, and credentials.
- **Role-Based Access Control**: Features three levels of access control - unauthenticated user, authenticated user, authenticated staff user, and authenticated super user.
- **Security Notice**: Please note that passwords are stored in plain text for this version. Exercise caution and consider implementing encryption for sensitive information.

## Deployment

The application can be deployed using Docker Compose. Below is a sample `docker-compose.yml` file to get you started:

```yaml
version: '3'

services:
  db:
    image: mysql:latest
    environment:
      MYSQL_DATABASE: 'hmlsvcrapp'
      MYSQL_USER: 'hmlsvcrapp'
      MYSQL_PASSWORD: 'hmlsvcrapp-password!'
      MYSQL_ROOT_PASSWORD: 'hmlsvcrapp-password!-root'
    volumes:
      - mysql_data:/var/lib/mysql
      - /createdatabase.sql:/docker-entrypoint-initdb.d
    ports:
      - "3306:3306"

  web:
    image: rherbaugh/homelabdatabase:latest
    ports:
      - "8001:8000"
    depends_on:
      - db
    environment:
      - DEBUG=1
      - DJANGO_SUPERUSER_USERNAME=admin
      - DJANGO_SUPERUSER_EMAIL=admin@example.com
      - DJANGO_SUPERUSER_PASSWORD=adminpassword
    command: >
      sh -c "sleep 60 &&
         python create_superuser.py &&
         python manage.py makemigrations &&
         python manage.py migrate &&
         python manage.py runserver 0.0.0.0:8000"

volumes:
  mysql_data:
```

**NOTE: Ensure to replace the placeholder values with your actual configuration details.**

## Contributing

As this project is a work in progress and my first venture into many of these technologies, I am very open to suggestions, contributions, and feedback to improve it. Feel free to fork the project, submit pull requests, or open issues on GitHub.

All code can be reviewed and contributed to on my GitHub: https://github.com/robertherbaugh/homelabdatabase.

Docker Hub Repository: https://hub.docker.com/r/rherbaugh/homelabdatabase

## Acknowledgements

A special thanks to ChatGPT for assisting in the development and documentation of this project. Your guidance has been invaluable.
