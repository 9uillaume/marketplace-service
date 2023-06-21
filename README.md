# Welcome to Marketplace

This is a Django-based Marketplace project that allows users to create categories and products. Products go through a state flow, starting from draft and transitioning to new. Once in the new state, products can be accepted, rejected, or banned by administrators.

The project utilizes the following technologies and tools:

- Django: A high-level Python web framework for rapid development.
- Celery: An asynchronous task queue/job queue based on distributed message passing.
- PostgreSQL: A powerful open-source relational database management system.
- Docker: A containerization platform for packaging applications and their dependencies.
- Django REST Framework: A powerful and flexible toolkit for building Web APIs.

## Project Structure

The project follows a typical Django project structure:
```
webapp/
├── marketplace/
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── item/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── ...
├── ...
└── ...
```

- The `marketplace/` directory contains the project-level settings and URL configuration.
- The `item/` directory contains the app for managing categories and products.

## Quickstart guide

Start the project:

    make up
    
and bring it down when you are down:

    make down
    
To test the project run:

    make test
    
To create an optimised production build do:

    make build VERSION=0.0.0
    
To push the optimised images to the registry do:

    make push VERSION=0.0.0


## Future Improvements

Here are some ideas for future improvements to enhance the project:

- Increase Test Coverage: Write more unit tests to cover different scenarios and edge cases and potential reports (file or Codecov)
- Improve API Documentation: Enhance the API documentation to provide comprehensive information and usage examples (Swagger)
- Implement CI/CD: Set up a CI/CD pipeline to automate build, test, and deployment processes.
- Logging and Error Handling: Implement a robust logging and error handling mechanism to identify and handle errors effectively.
- Scalability and Performance: Optimize the application for better performance and scalability as the user base grows.
- Security Measures: Implement additional security measures such as rate limiting, authentication/authorization improvements, and data encryption.
- User Interface: Enhance the user interface for a better user experience (admin UI)
- Monitoring and Alerting: Implement monitoring and alerting mechanisms to proactively detect and resolve issues.