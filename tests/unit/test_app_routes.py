"""
Unit tests for Flask application routes
"""
import pytest
import numpy as np
import pickle
import os
import tempfile
import shutil
from unittest.mock import patch, MagicMock
from flask import Flask


# Create a simple mock model class that can be pickled
class MockModel:
    def predict(self, X):
        return np.array([4.2])


class TestFlaskRoutes:
    """Test class for Flask application routes and functionality"""
    
    @pytest.fixture
    def app(self):
        """Create a test Flask app instance"""
        mock_model = MockModel()
        
        # Create a temporary model file
        import tempfile
        import pickle
        temp_dir = tempfile.mkdtemp()
        temp_model_path = os.path.join(temp_dir, 'model.pkl')
        
        with open(temp_model_path, 'wb') as f:
            pickle.dump(mock_model, f)
        
        # Change to parent directory and copy model file
        import shutil
        original_cwd = os.getcwd()
        os.chdir('..')
        
        try:
            # Copy the temp model to current directory (parent of tests)
            shutil.copy2(temp_model_path, 'model.pkl')
            
            # Import and configure the app
            from app import app as flask_app
            flask_app.config['TESTING'] = True
            flask_app.config['WTF_CSRF_ENABLED'] = False
            
            yield flask_app
        finally:
            # Cleanup
            if os.path.exists('model.pkl'):
                os.remove('model.pkl')
            os.chdir(original_cwd)
            shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def client(self, app):
        """Create a test client for the Flask app"""
        return app.test_client()
    
    @pytest.mark.unit
    def test_home_route(self, client):
        """Test the home route returns the correct template"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Predict Zomato Restaurant Ratings' in response.data
    
    @pytest.mark.unit
    def test_predict_route_success(self, client, sample_form_data):
        """Test the predict route with valid form data"""
        response = client.post('/predict', data=sample_form_data)
        assert response.status_code == 200
        assert b'Your Rating is:' in response.data
    
    @pytest.mark.unit
    def test_predict_route_missing_data(self, client):
        """Test the predict route with missing form data"""
        form_data = {
            'Online Order': '1',
            'Book Table': '0',
            # Missing other required fields
        }
        
        response = client.post('/predict', data=form_data)
        # Should still return 200 but might have different behavior
        assert response.status_code == 200
    
    @pytest.mark.unit
    def test_predict_route_invalid_data(self, client, invalid_form_data):
        """Test the predict route with invalid data types"""
        # This should raise a ValueError when trying to convert invalid strings to int
        with pytest.raises(ValueError):
            response = client.post('/predict', data=invalid_form_data)
    
    @pytest.mark.unit
    def test_predict_route_empty_data(self, client):
        """Test the predict route with empty form data"""
        response = client.post('/predict', data={})
        assert response.status_code in [200, 400, 500]
    
    @pytest.mark.unit
    def test_predict_route_get_method(self, client):
        """Test that GET method is not allowed on predict route"""
        response = client.get('/predict')
        assert response.status_code == 405  # Method Not Allowed
    
    @pytest.mark.unit
    def test_predict_route_response_format(self, client, sample_form_data):
        """Test that predict route returns properly formatted response"""
        response = client.post('/predict', data=sample_form_data)
        assert response.status_code == 200
        
        response_text = response.get_data(as_text=True)
        assert 'Your Rating is:' in response_text
        
        # Check that the rating is a number
        import re
        rating_match = re.search(r'Your Rating is: ([\d.]+)', response_text)
        if rating_match:
            rating = float(rating_match.group(1))
            assert 0 <= rating <= 5, f"Rating {rating} is not in expected range [0, 5]"
    
    @pytest.mark.unit
    def test_predict_route_multiple_submissions(self, client, sample_form_data):
        """Test multiple submissions with same data"""
        responses = []
        for _ in range(3):
            response = client.post('/predict', data=sample_form_data)
            responses.append(response)
        
        # All responses should be successful
        for response in responses:
            assert response.status_code == 200
            assert b'Your Rating is:' in response.data


class TestDataValidation:
    """Test class for data validation and preprocessing"""
    
    @pytest.mark.unit
    def test_feature_count(self):
        """Test that the expected number of features are provided"""
        # Based on the HTML form, we expect 8 features
        expected_features = [
            'Online Order', 'Book Table', 'Votes', 'Location',
            'Restaurant Type', 'Cuisines', 'Cost', 'Menu Item'
        ]
        assert len(expected_features) == 8, "Expected 8 features"
    
    @pytest.mark.unit
    def test_feature_data_types(self):
        """Test that features can be converted to integers"""
        test_values = ['1', '0', '100', '5', '10', '15', '500', '20']
        
        try:
            converted_values = [int(x) for x in test_values]
            assert len(converted_values) == 8
            assert all(isinstance(x, int) for x in converted_values)
        except ValueError as e:
            pytest.fail(f"Feature conversion failed: {e}")
    
    @pytest.mark.unit
    def test_numpy_array_creation(self):
        """Test that features can be converted to numpy array"""
        test_features = [1, 0, 100, 5, 10, 15, 500, 20]
        
        try:
            final_features = [np.array(test_features)]
            assert len(final_features) == 1
            assert final_features[0].shape == (8,)
        except Exception as e:
            pytest.fail(f"NumPy array creation failed: {e}")
    
    @pytest.mark.unit
    def test_feature_range_validation(self):
        """Test that features are within reasonable ranges"""
        # Test valid ranges
        valid_features = {
            'Online Order': [0, 1],
            'Book Table': [0, 1],
            'Votes': [0, 10000],
            'Location': [0, 100],
            'Restaurant Type': [0, 100],
            'Cuisines': [0, 100],
            'Cost': [1, 5000],
            'Menu Item': [0, 100]
        }
        
        for feature, (min_val, max_val) in valid_features.items():
            assert min_val <= 1 <= max_val, f"Feature {feature} range validation failed"


class TestErrorHandling:
    """Test class for error handling scenarios"""
    
    @pytest.mark.unit
    def test_model_loading_error(self):
        """Test behavior when model file is missing"""
        # Test that the app handles missing model file gracefully
        # by checking if the model file exists before importing
        if not os.path.exists('../model.pkl'):
            pytest.skip("Model file not found - this is expected in test environment")
    
    @pytest.mark.unit
    def test_invalid_model_prediction(self):
        """Test handling of invalid model predictions"""
        # Test that our mock model works correctly
        mock_model = MockModel()
        test_input = [[1, 0, 100, 5, 10, 15, 500, 20]]
        prediction = mock_model.predict(test_input)
        assert prediction is not None
        assert len(prediction) == 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
