# Demo-RAG

## Overview

This repository contains the codebase for a scalable, modular application built using FastAPI, adhering to Clean Architecture principles. The project is structured to enhance maintainability, testability, and scalability by decoupling business logic from external frameworks and infrastructure. With dependency injection and event-driven architecture, the application promotes separation of concerns, making it resilient to change and easy to extend.

Key components of this architecture include:
- `pydiator` for implementing the mediator pattern, managing requests and commands for streamlined interactions.
- `fastapi-injector` for dependency injection, enabling modular service configuration and enhancing testability.
- `pymilvus` or `postgresql` for database interactions, facilitating robust and efficient handling of vector data in AI-driven applications.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Configuration](#configuration)
3. [Usage](#usage)
4. [Project Structure](#project-structure)
5. [Understanding Key Components](#understanding-key-components)
   - [pydiator](#pydiator)
   - [fastapi-injector](#fastapi-injector)

---

### Getting Started with docker

1. **Clone the Repository**
    ```bash
    git clone <repository-url>
    cd demo-rag
    ```

2. **Environment Configuration**
   - Copy the example environment file to a new `.env` file and fill in any necessary values:
     ```bash
     cp .env.example .env
     ```

3. **Build and Run with Docker**
   - Start the application with Docker Compose:
     ```bash
     docker-compose up --build
     ```

### Getting Started without Docker

1. **Clone the Repository**
   - Start by cloning the repository and navigating to the project directory:
     ```bash
     git clone <repository-url>
     cd demo-rag
     ```

2. **Configure the Environment**
   - Copy the example environment file to create a new `.env` file, then fill in any necessary configuration values:
     ```bash
     cp .env.example .env
     ```

3. **Set Up PostgreSQL with PGVector**
   - Ensure that PostgreSQL is running on your system and that the PGVector extension is installed and enabled. This extension is required for efficient vector data handling within the database.

4. **Run the Application**
   - Start the FastAPI application in development mode using Uvicorn:
     ```bash
     uvicorn app.main:app --reload
     ```

After completing these steps, the application will be accessible locally, typically at [http://localhost:8000](http://localhost:8000). You can explore the API documentation and interact with the endpoints via the Swagger UI, available at `/docs`.

### Configuration

- Ensure that the `.env` file is configured with the required environment variables.

### Usage

After starting the application, it will be accessible at the default FastAPI port (usually [http://localhost:8000](http://localhost:8000)). You can interact with any exposed endpoints and explore the API's documentation via Swagger (typically available at `/docs`).

### Project Structure

The application is organized as follows:
- `app/`: Contains the main FastAPI app and route definitions.
- `ai_engine/`: Contains isolated modules specific to the AI engine, including routes, handlers, and utilities.

### Understanding Key Components

#### `pydiator` (Mediator Pattern Implementation)

`pydiator` is a Python library that helps implement the Mediator pattern, promoting separation of concerns by managing how requests and commands are processed. In this project:

#### `fastapi-injector` (Dependency Injection for FastAPI)

`fastapi-injector` is a dependency injection framework tailored for FastAPI, simplifying dependency management:
- **Dependency Injection** decouples class instantiation from service configuration, allowing better modularization and facilitating testing.
- With `fastapi-injector`, dependencies (like database connections or shared services) are injected directly into route handlers or classes, enhancing code readability and reusability.

Using `fastapi-injector`, you can configure dependencies centrally, ensuring consistent and efficient resource management across the application.

---

### Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydiator Documentation](https://github.com/ozgurkara/pydiator-core)
- [Fastapi-injector GitHub](https://github.com/matyasrichter/fastapi-injector)
- [Quickstart review Milvus](https://milvus.io/docs/quickstart.md)

---
