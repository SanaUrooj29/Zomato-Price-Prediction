"""
Environment and setup tests to verify the testing environment is working correctly
"""
import pytest
import os
import sys


class TestEnvironmentSetup:
    """Test that the testing environment is set up correctly"""
    
    @pytest.mark.unit
    def test_environment_setup(self):
        """Test that the testing environment is set up correctly"""
        assert os.path.exists('../app.py'), "app.py should exist"
        assert os.path.exists('../model.py'), "model.py should exist"
        assert os.path.exists('../requirements.txt'), "requirements.txt should exist"
    
    @pytest.mark.unit
    def test_model_file_exists(self):
        """Test that the model file exists"""
        # Skip this test if model file doesn't exist (common in test environments)
        if not os.path.exists('../model.pkl'):
            pytest.skip("Model file 'model.pkl' not found. Run model.py to generate it.")
        assert os.path.exists('../model.pkl'), "model.pkl should exist"
    
    @pytest.mark.unit
    def test_dataset_exists(self):
        """Test that the dataset exists"""
        assert os.path.exists('../zomato_df.csv'), "zomato_df.csv should exist"
    
    @pytest.mark.unit
    def test_templates_exist(self):
        """Test that template files exist"""
        assert os.path.exists('../templates/index.html'), "templates/index.html should exist"
    
    @pytest.mark.unit
    def test_static_files_exist(self):
        """Test that static files exist"""
        assert os.path.exists('../static/css/style.css'), "static/css/style.css should exist"
    
    @pytest.mark.unit
    def test_basic_math(self):
        """Simple unit test to verify pytest is working"""
        assert 2 + 2 == 4
        assert 3 * 3 == 9
    
    @pytest.mark.unit
    def test_imports(self):
        """Test that all required modules can be imported"""
        try:
            import flask
            import numpy as np
            import pandas as pd
            import sklearn
            import pickle
            import pytest
            assert True
        except ImportError as e:
            pytest.fail(f"Failed to import required module: {e}")
    
    @pytest.mark.unit
    def test_python_version(self):
        """Test that we're using a compatible Python version"""
        version = sys.version_info
        assert version.major == 3, f"Expected Python 3, got {version.major}"
        assert version.minor >= 8, f"Expected Python 3.8+, got {version.major}.{version.minor}"
    
    @pytest.mark.unit
    def test_working_directory(self):
        """Test that we're in the correct working directory"""
        current_dir = os.getcwd()
        assert 'FLASK-End-to-end-Zomato-Restaurant-Price-Prediction-and-Deployment' in current_dir, \
            f"Not in correct directory: {current_dir}"
    
    @pytest.mark.unit
    def test_tests_directory_structure(self):
        """Test that the tests directory structure is correct"""
        assert os.path.exists('.'), "tests directory should exist"
        assert os.path.exists('unit'), "tests/unit directory should exist"
        assert os.path.exists('integration'), "tests/integration directory should exist"
        assert os.path.exists('conftest.py'), "tests/conftest.py should exist"
    
    @pytest.mark.unit
    def test_test_files_exist(self):
        """Test that all test files exist"""
        test_files = [
            'unit/test_app_routes.py',
            'unit/test_model_validation.py',
            'integration/test_app_integration.py',
            'test_environment.py'
        ]
        
        for test_file in test_files:
            assert os.path.exists(test_file), f"Test file {test_file} should exist"
    
    @pytest.mark.unit
    def test_configuration_files_exist(self):
        """Test that configuration files exist"""
        config_files = [
            'pytest.ini',
            'conftest.py',
            'run_tests.py'
        ]
        
        for config_file in config_files:
            assert os.path.exists(config_file), f"Configuration file {config_file} should exist"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
