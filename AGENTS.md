# AGENT Instructions for hobbyhosting

This file provides guidance for automated agents working with this repository.

## Testing
- Run `make test` to execute all Python and JavaScript tests.

## Linting and formatting
- Run `make lint` for lint checks.
- Run `make format` to automatically format the code.
- A `.pre-commit-config.yaml` is provided; use `pre-commit run --files <file1> <file2>` when committing small changes.

## Commit and PR guidelines
- Ensure `make lint` and `make test` pass before committing.
- Keep commit messages short and descriptive.
- Summaries for PRs should describe the main changes and mention test results.

## Repository structure
- `services/` contains backend services such as `auth_service`.
- `apps/` holds frontend applications.
- Use the `Makefile` for common tasks like rebuilding Docker containers or viewing logs.
