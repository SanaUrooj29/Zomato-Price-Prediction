# Tests for Zomato Restaurant Price Prediction Application

This directory contains comprehensive tests for the Flask-based Zomato restaurant price prediction application.

## Directory Structure

```
tests/
├── __init__.py
├── conftest.py              # Pytest configuration and shared fixtures
├── pytest.ini              # Pytest settings
├── run_tests.py            # Test runner script
├── README.md               # This file
├── test_environment.py     # Environment and setup tests
├── unit/                   # Unit tests
│   ├── __init__.py
│   ├── test_app_routes.py      # Flask route tests
│   └── test_model_validation.py # Model validation tests
├── integration/            # Integration tests
│   ├── __init__.py
│   └── test_app_integration.py # End-to-end application tests
├── fixtures/               # Test fixtures and sample data
│   └── sample_data.py      # Sample data for testing
└── data/                   # Test data files (if needed)
```

## Test Categories

### 1. Unit Tests (`unit/`)
- **test_app_routes.py**: Tests Flask application routes and functionality
  - Home route testing
  - Predict route testing with various inputs
  - Error handling scenarios
  - Data validation tests

- **test_model_validation.py**: Tests model functionality and validation
  - Model type and parameter validation
  - Prediction output validation
  - Performance metrics testing
  - Data quality checks
  - Model robustness testing

### 2. Integration Tests (`integration/`)
- **test_app_integration.py**: End-to-end application testing
  - Complete prediction flow testing
  - Multiple prediction consistency
  - Different input scenarios
  - Performance under load
  - Error handling integration

### 3. Environment Tests
- **test_environment.py**: Environment and setup validation
  - File existence checks
  - Import validation
  - Directory structure validation
  - Configuration file validation

## Running Tests

### Prerequisites
1. Activate the virtual environment:
   ```bash
   source bin/activate
   ```

2. Install test dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running All Tests
```bash
# From the project root directory
python run_tests.py

# Or from the tests directory
cd tests
python run_tests.py
```

### Running Specific Test Types
```bash
# Unit tests only
python run_tests.py --type unit

# Integration tests only
python run_tests.py --type integration

# Model validation tests only
python run_tests.py --type model
```

### Running with Coverage
```bash
# Generate coverage report
python run_tests.py --coverage

# Coverage report will be generated in htmlcov/index.html
```

### Running Specific Test Files
```bash
# Run a specific test file
python run_tests.py --file test_app_routes.py

# Run tests with specific markers
python run_tests.py --markers "unit and not slow"
```

### Using pytest directly
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest test_environment.py

# Run tests with specific markers
pytest -m unit
pytest -m integration
pytest -m "not slow"
```

## Test Markers

Tests are organized using pytest markers:

- `@pytest.mark.unit`: Unit tests
- `@pytest.mark.integration`: Integration tests
- `@pytest.mark.model`: Model validation tests
- `@pytest.mark.slow`: Slow-running tests

## Test Fixtures

The `conftest.py` file provides shared fixtures:

- `sample_model`: Mock model for testing
- `sample_data`: Sample data for testing
- `sample_form_data`: Sample form data
- `invalid_form_data`: Invalid data for error testing
- `app_config`: Application configuration for testing

## Sample Data

The `fixtures/sample_data.py` file provides:

- Sample restaurant data
- Form data for testing
- Edge case data
- Invalid data for error handling
- Performance test data

## Coverage

The tests aim for high code coverage. Coverage reports are generated in HTML format and can be viewed in `htmlcov/index.html`.

## Continuous Integration

These tests are designed to be run in CI/CD pipelines. The test runner script provides appropriate exit codes for automation.

## Troubleshooting

### Common Issues

1. **Model file not found**: Run `python model.py` to generate the model file
2. **Dataset not found**: Ensure `zomato_df.csv` is in the project root
3. **Import errors**: Make sure the virtual environment is activated and dependencies are installed
4. **Permission errors**: Ensure test files are executable (`chmod +x run_tests.py`)

### Debug Mode

Run tests with verbose output for debugging:
```bash
python run_tests.py --verbose
```

### Test Development

When adding new tests:

1. Follow the existing naming conventions
2. Add appropriate markers
3. Use existing fixtures when possible
4. Add docstrings explaining test purpose
5. Update this README if adding new test categories

## Performance Considerations

- Unit tests should run quickly (< 1 second each)
- Integration tests may take longer but should complete within reasonable time
- Slow tests are marked with `@pytest.mark.slow`
- Performance tests are included to ensure the application can handle load

## Best Practices

1. **Test Isolation**: Each test should be independent
2. **Clear Naming**: Test names should clearly describe what is being tested
3. **Assertions**: Use specific assertions with clear error messages
4. **Fixtures**: Use fixtures for common setup/teardown
5. **Mocking**: Mock external dependencies when appropriate
6. **Coverage**: Aim for high test coverage of critical paths
