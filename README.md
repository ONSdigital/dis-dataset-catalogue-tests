# dis-dataset-catalogue-tests

Smoke tests for the dataset catalogue. These are happy path tests designed to ensure core capability remains unaffected by changes deployed to our services

## Getting started

### Dependencies

- [pyenv](https://github.com/pyenv/pyenv) - Python version management
- [Python 3.14.3](https://www.python.org/) - Install via pyenv: `pyenv install 3.14.3`
- [Poetry](https://python-poetry.org/) - Dependency management
- [dp-compose](https://github.com/ONSdigital/dp-compose) - Docker compose stack for running services locally

### Running locally

Install dependencies:

```bash
poetry install
```

Run tests:

```bash
poetry run pytest
```

### Configuration

## Contributing

See [CONTRIBUTING](CONTRIBUTING.md) for details.

## License

Copyright © 2026, Office for National Statistics (<https://www.ons.gov.uk>)

Released under MIT license, see [LICENSE](LICENSE.md) for details.