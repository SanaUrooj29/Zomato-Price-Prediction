"""
Pytest configuration and shared fixtures for the Zomato Restaurant Price Prediction tests
"""
import pytest
import os
import tempfile
import shutil
import pickle
import numpy as np
from unittest.mock import MagicMock


@pytest.fixture(scope="session")
def test_data_dir():
    """Create a temporary directory for test data"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture(scope="session")
def sample_model():
    """Create a sample model for testing"""
    # Create a mock ExtraTreesRegressor model
    mock_model = MagicMock()
    mock_model.predict.return_value = np.array([4.2])
    mock_model.n_estimators = 120
    mock_model.feature_importances_ = np.array([0.1, 0.2, 0.15, 0.1, 0.1, 0.1, 0.15, 0.1])
    
    return mock_model


@pytest.fixture(scope="session")
def sample_data():
    """Create sample data for testing"""
    return {
        'features': [1, 0, 100, 5, 10, 15, 500, 20],
        'expected_rating_range': (0, 5),
        'feature_names': [
            'Online Order', 'Book Table', 'Votes', 'Location',
            'Restaurant Type', 'Cuisines', 'Cost', 'Menu Item'
        ]
    }


@pytest.fixture
def mock_model_file(test_data_dir, sample_model):
    """Create a temporary model file for testing"""
    model_path = os.path.join(test_data_dir, 'test_model.pkl')
    
    with open(model_path, 'wb') as f:
        pickle.dump(sample_model, f)
    
    return model_path


@pytest.fixture
def app_config():
    """Application configuration for testing"""
    return {
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': 'test-secret-key'
    }


# Pytest hooks
def pytest_configure(config):
    """Configure pytest with custom settings"""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "model: mark test as a model validation test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test names"""
    for item in items:
        # Add markers based on test file names
        if "test_model" in item.nodeid:
            item.add_marker(pytest.mark.model)
        elif "test_app" in item.nodeid:
            if "integration" in item.name.lower():
                item.add_marker(pytest.mark.integration)
            else:
                item.add_marker(pytest.mark.unit)
        
        # Add slow marker for performance tests
        if "performance" in item.name.lower() or "robustness" in item.name.lower():
            item.add_marker(pytest.mark.slow)
