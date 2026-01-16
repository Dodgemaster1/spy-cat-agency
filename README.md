# Spy Cat Agency (SCA) Management System

The **Spy Cat Agency (SCA)** management system is a RESTful API application designed to streamline the operations of the agency. It enables the management of spy cats, their missions, and assigned targets.

## Features

### Spy Cats
- **Manage Cats**: Create, list, retrieve, and delete spy cats.
- **Attributes**: Name, years of experience, breed, and salary.
- **Breed Validation**: Automatically validates cat breeds against [TheCatAPI](https://api.thecatapi.com/v1/breeds) upon creation.
- **Salary Update**: Ability to update a cat's salary.

### Missions & Targets
- **Mission Management**: Create missions with multiple targets (1-3 max).
- **Target Tracking**: Each mission consists of unique targets with details like name, country, notes, and completion status.
- **Assignment**: Assign missions to available spy cats. A cat can only handle one active mission at a time.
- **Progress Tracking**: 
    - Mark targets as complete.
    - Update notes on targets (notes are frozen once the target or mission is completed).
    - Mission is automatically marked as complete when all targets are done.
- **Deletion**: Delete missions (restricted if already assigned to a cat).

## Tech Stack

- **Language**: Python 3.14
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database**: PostgreSQL (with `psycopg` async driver)
- **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/) (Async)
- **Dependency Injection**: [Dishka](https://github.com/reagento/dishka)
- **Validation**: [Pydantic](https://docs.pydantic.dev/)
- **Package Manager**: [uv](https://github.com/astral-sh/uv)
- **Containerization**: Docker & Docker Compose

## Running the Application

### Prerequisites
- Docker and Docker Compose installed.

### Setup

1.  **Environment Variables**
    Copy the example environment files (if available) or create `.env` and `.env.docker`:
    ```bash
    cp .env.example .env
    ```
    Ensure you define necessary variables like `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, and `GRANIAN_PORT`.

2.  **Start with Docker Compose**
    Run the application and database containers:
    ```bash
    docker-compose up --build
    ```

    The application will be available at `http://localhost:<GRANIAN_PORT>`.

3.  **Migrations**
    Migrations run automatically on startup via the `migrations` service defined in `compose.yaml`.

## API Documentation

Once the application is running, you can access the interactive API documentation at:

- **Swagger UI**: `http://localhost:<GRANIAN_PORT>/docs`
- **Redoc**: `http://localhost:<GRANIAN_PORT>/redoc`

## Development

To run the project locally without Docker for development:

1.  **Install Dependencies**
    ```bash
    uv sync
    ```

2.  **Run Locally**
    Use `just` to run development commands (see `justfile` for details):
    ```bash
    just start
    ```
    Or run migrations:
    ```bash
    just migrate
    ```

3.  **Linting & Testing**
    ```bash
    just lint
    just typecheck
    ```
