set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]

[doc("All command information")]
default:
  @just --list --unsorted --list-heading $'Taskum commands…\n'

alias l := lint
lint:
    uv run ruff format src pyproject.toml alembic
    uv run ruff check src pyproject.toml alembic --fix
    uv run ruff format src pyproject.toml alembic

alias tc := typecheck
typecheck:
    uv run mypy src tests

alias s := start
start:
    uv run --env-file=.env granian src.main:task_app

migrate:
    uv run --env-file=.env alembic upgrade head
