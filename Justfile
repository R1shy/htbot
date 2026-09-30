set shell := ["bash", "-c"]

default:
    @just --list

check: format-check lint type-check

fix: format lint-fix

run:
    uv run hades

format-check:
    uv run ruff format --check .

format:
    uv run ruff format .

type-check:
    uv run pyright .

lint:
    uv run ruff check .

lint-fix:
    uv run ruff check --fix .

clean:
    rm -rf .ruff_cache .pyrightpy .pytest_cache
    find . -type d -name "__pycache__" -exec rm -r {} +
