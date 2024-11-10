# AppPython

## Description

An app to show time in GMT+3 time zone.

## Features

- templates
- justfile
- cozy website design
- mocked datetime.datetime

## how to run

### Prerequisites

Install [just](https://github.com/casey/just) it is really awesome. Or run scripts from it manually

### Run app

1. go to `app_python`
2. `just run`

## Entrypoints

- `/` - home page
- `/time` - get time in GMT+3 time zone
- `/docs` - swagger (openapi) specification

## Unit Tests

The application uses pytest as its testing framework. Key testing details:

- Tests are located in the `/tests` directory
- Tests ensure correct application behavior
- Run tests easily using the command `just test`
- Testing follows PEP 8 standards using IDE formatter

## CI/CD Pipeline

This project uses GitHub Actions for continuous integration and delivery. The workflow includes:

### Python CI Steps
- **Dependencies**: Installs all required Python packages
- **Linting**: Uses flake8 to ensure code quality
- **Testing**: Runs pytest suite

### Docker Steps
- **Registry Login**: Authenticates with GitHub Container Registry
- **Build & Push**: Builds and pushes Docker image to ghcr.io

The workflow runs on every push to main and on pull requests. You can view the workflow status in the Actions tab of the repository.
