# Demo-RAG

## Overview

This repository contains the codebase for a scalable, modular application built using FastAPI, with dependency injection and event-driven architecture principles. The project leverages `pydiator` for implementing the mediator pattern, `fastapi-injector` for dependency injection, and `pymilvus` for database interactions.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Configuration](#configuration)
3. [Usage](#usage)
4. [Project Structure](#project-structure)
5. [Understanding Key Components](#understanding-key-components)
   - [pydiator](#pydiator)
   - [fastapi-injector](#fastapi-injector)

---

### Getting Started

1. **Clone the Repository**
    ```bash
    git clone <repository-url>
    cd demo-rag
    ```

2. **Environment Configuration**
   - Copy the example environment file to a new `.env` file and fill in any necessary values:
     ```bash
     cp .example.env .env
     ```

3. **Build and Run with Docker**
   - Start the application with Docker Compose:
     ```bash
     docker-compose up --build
     ```

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
- [pydiator Documentation](https://github.com/ozgurkara/pydiator-core)
- [fastapi-injector GitHub](https://github.com/matyasrichter/fastapi-injector)

---