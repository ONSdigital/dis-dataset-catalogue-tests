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

Install Playwright browsers:

```bash
poetry run playwright install
```

Run tests:

```bash
poetry run behave
```

Or using make:

```bash
make test
```

### Debugging behaviour tests

Use the `behave_debug.py` script in the root of the repo to debug behaviour tests. There are 3 arguments in the `args` list. The first argument specifies the file path of the feature file to be debugged. The second and third arguments allow you to set a specific scenario within the feature file that you want to debug. Comment out these arguments to debug all scenarios in the specified feature file. Set breakpoints in the step definition functions to inspect variables and context values at each step.

### Configuration

## Contributing

See [CONTRIBUTING](CONTRIBUTING.md) for details.

## License

Copyright © 2026, Office for National Statistics (<https://www.ons.gov.uk>)

Released under MIT license, see [LICENSE](LICENSE.md) for details.