set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]

[doc("All command information")]
default:
  @just --list --unsorted --list-heading $'Taskum commands…\n'

alias l := lint
[group("local")]
[doc("Check and format code with autofix (in pyproject.toml src/ tests/ alembic/) using ruff")]
lint:
    uv run ruff format src pyproject.toml alembic
    uv run ruff check src pyproject.toml alembic --fix
    uv run ruff format src pyproject.toml alembic

alias tc := typecheck
[group("local")]
[group("ci")]
[doc("Check types (in src/ and tests/) using mypy")]
typecheck:
    uv run mypy src tests

[group("local")]
[doc("Run lint and typecheck")]
check: lint typecheck

alias s := start
[group("local")]
[doc("Start the development server (use .env for environment variables)")]
start:
    uv run --env-file=.env granian src.main:task_app

[group("local")]
[doc("Run database migrations to the latest revision")]
migrate:
    uv run --env-file=.env alembic upgrade head

[group("local")]
[doc("Start the Celery worker (use .env for environment variables)")]
celery:
    uv run --env-file=.env celery -A src.celery.app worker --loglevel=INFO

[group("local")]
[doc("Start the Celery Flower monitoring tool (use .env for environment variables)")]
celery-flower:
    uv run --env-file=.env celery -A src.celery.app flower


[group("prod")]
[doc("Start the production server without dev dependencies (use .env and .env.docker for environment variables)")]
prod-start:
    uv run --no-dev --env-file ".env .env.docker" granian src.main:task_app

[group("prod")]
[doc("Run database migrations to the latest revision without dev dependencies")]
prod-migrate:
    uv run --no-dev --env-file ".env .env.docker" alembic upgrade head

[group("prod")]
[doc("Start the Celery worker (use .env for environment variables)")]
prod-celery:
    uv run --no-dev --env-file ".env .env.docker" celery -A src.celery.app worker --loglevel=INFO

[group("prod")]
[doc("Start the Celery Flower monitoring tool (use .env for environment variables)")]
prod-celery-flower:
    uv run --no-dev --env-file ".env .env.docker" celery -A src.celery.app flower


[group("ci")]
[doc("Check and format code without autofix (in pyproject.toml src/ tests/ alembic/) using ruff")]
ci-lint:
    uv run ruff format src pyproject.toml tests alembic --diff
    uv run ruff check src pyproject.toml tests alembic --output-format=github
    uv run ruff format src pyproject.toml tests alembic --diff

[group("ci")]
[doc("Run tests for CI")]
ci-test:
    uv run pytest -vv -s --record-mode=none


[group("ci")]
[doc("Run lint and typecheck for CI")]
ci-check: ci-lint typecheck


[group("scripts")]
[doc("Generate a base64 string from .env and .env.docker on linux")]
gen-env-linux:
    base64 .env
    base64 .env.docker

[group("scripts")]
[doc("Generate a base64 string from .env and .env.docker on macos")]
gen-env-mac:
    base64 -i .env
    base64 -i .env.docker


[group("docker")]
[group("local")]
[doc("Run tests in Docker container with --build option (use compose-test.yaml)")]
run-tests:
    docker compose -f compose-test.yaml run --build --rm tests
    docker compose -f compose-test.yaml down -v

[group("docker")]
[group("ci")]
[doc("Run tests in Docker container for CI (use compose-test.yaml)")]
ci-run-tests:
    docker compose -f compose-test.yaml run --rm tests
    docker compose -f compose-test.yaml down -v
