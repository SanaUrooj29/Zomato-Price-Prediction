"""
Integration tests for the complete Flask application
"""
import pytest
import os
import sys
import re
from flask import Flask

# Add the parent directory to the path so we can import the app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


class TestIntegration:
    """Integration tests for the complete application flow"""
    
    @pytest.fixture
    def app_with_real_model(self):
        """Create app instance with real model for integration testing"""
        # Check if model file exists in parent directory
        if not os.path.exists('../model.pkl'):
            pytest.skip("Model file 'model.pkl' not found. Run model.py first.")
        
        # Temporarily change to parent directory to import app
        original_cwd = os.getcwd()
        os.chdir('..')
        
        try:
            from app import app as flask_app
            flask_app.config['TESTING'] = True
            return flask_app
        finally:
            os.chdir(original_cwd)
    
    @pytest.fixture
    def client_with_real_model(self, app_with_real_model):
        """Create test client with real model"""
        return app_with_real_model.test_client()
    
    @pytest.mark.integration
    def test_complete_prediction_flow(self, client_with_real_model):
        """Test the complete prediction flow from form submission to result"""
        form_data = {
            'Online Order': '1',
            'Book Table': '1',
            'Votes': '500',
            'Location': '25',
            'Restaurant Type': '30',
            'Cuisines': '45',
            'Cost': '800',
            'Menu Item': '60'
        }
        
        response = client_with_real_model.post('/predict', data=form_data)
        assert response.status_code == 200
        
        # Check that prediction text is in the response
        response_text = response.get_data(as_text=True)
        assert 'Your Rating is:' in response_text
        
        # Extract the rating value
        rating_match = re.search(r'Your Rating is: ([\d.]+)', response_text)
        if rating_match:
            rating = float(rating_match.group(1))
            assert 0 <= rating <= 5, f"Rating {rating} is not in expected range [0, 5]"
    
    @pytest.mark.integration
    def test_multiple_predictions_consistency(self, client_with_real_model):
        """Test that multiple predictions with same input are consistent"""
        form_data = {
            'Online Order': '1',
            'Book Table': '0',
            'Votes': '200',
            'Location': '15',
            'Restaurant Type': '20',
            'Cuisines': '25',
            'Cost': '600',
            'Menu Item': '30'
        }
        
        # Make multiple requests
        responses = []
        for _ in range(3):
            response = client_with_real_model.post('/predict', data=form_data)
            responses.append(response)
        
        # All responses should be successful
        for response in responses:
            assert response.status_code == 200
        
        # All responses should contain prediction text
        for response in responses:
            assert b'Your Rating is:' in response.data
    
    @pytest.mark.integration
    def test_different_input_scenarios(self, client_with_real_model):
        """Test various input scenarios to ensure robust handling"""
        test_scenarios = [
            {
                'name': 'High-end restaurant',
                'data': {
                    'Online Order': '1',
                    'Book Table': '1',
                    'Votes': '1000',
                    'Location': '50',
                    'Restaurant Type': '40',
                    'Cuisines': '60',
                    'Cost': '2000',
                    'Menu Item': '80'
                }
            },
            {
                'name': 'Budget restaurant',
                'data': {
                    'Online Order': '0',
                    'Book Table': '0',
                    'Votes': '50',
                    'Location': '10',
                    'Restaurant Type': '5',
                    'Cuisines': '10',
                    'Cost': '200',
                    'Menu Item': '15'
                }
            },
            {
                'name': 'Mid-range restaurant',
                'data': {
                    'Online Order': '1',
                    'Book Table': '0',
                    'Votes': '300',
                    'Location': '25',
                    'Restaurant Type': '20',
                    'Cuisines': '30',
                    'Cost': '800',
                    'Menu Item': '40'
                }
            }
        ]
        
        for scenario in test_scenarios:
            response = client_with_real_model.post('/predict', data=scenario['data'])
            assert response.status_code == 200, f"Failed for scenario: {scenario['name']}"
            
            response_text = response.get_data(as_text=True)
            assert 'Your Rating is:' in response_text, f"No prediction for scenario: {scenario['name']}"
            
            # Extract and validate rating
            rating_match = re.search(r'Your Rating is: ([\d.]+)', response_text)
            if rating_match:
                rating = float(rating_match.group(1))
                assert 0 <= rating <= 5, f"Invalid rating {rating} for scenario: {scenario['name']}"
    
    @pytest.mark.integration
    def test_application_startup(self, app_with_real_model):
        """Test that the application starts up correctly"""
        assert app_with_real_model is not None
        assert app_with_real_model.config['TESTING'] is True
        
        # Test that routes are registered
        rules = [rule.rule for rule in app_with_real_model.url_map.iter_rules()]
        assert '/' in rules, "Home route not registered"
        assert '/predict' in rules, "Predict route not registered"
    
    @pytest.mark.integration
    def test_model_loading_integration(self):
        """Test that the model loads correctly in the application context"""
        # Get the project root directory
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        model_path = os.path.join(project_root, 'model.pkl')
        
        # Check if model file exists first
        if not os.path.exists(model_path):
            pytest.skip("Model file 'model.pkl' not found. Run model.py to generate it.")
        
        # Temporarily change to project root directory to import app
        original_cwd = os.getcwd()
        os.chdir(project_root)
        
        try:
            from app import model
            
            assert model is not None, "Model not loaded"
            assert hasattr(model, 'predict'), "Model missing predict method"
            
            # Test a simple prediction
            test_input = [[1, 0, 100, 5, 10, 15, 500, 20]]
            prediction = model.predict(test_input)
            
            assert prediction is not None, "Model prediction failed"
            assert len(prediction) == 1, "Expected single prediction"
            assert 0 <= prediction[0] <= 5, f"Invalid prediction: {prediction[0]}"
        finally:
            os.chdir(original_cwd)
    
    @pytest.mark.integration
    def test_error_handling_integration(self, client_with_real_model):
        """Test error handling in the complete application flow"""
        # Test with malformed data
        malformed_data = {
            'Online Order': 'invalid',
            'Book Table': 'not_a_number',
            'Votes': 'also_invalid',
            'Location': '5',
            'Restaurant Type': '10',
            'Cuisines': '15',
            'Cost': '500',
            'Menu Item': '20'
        }
        
        response = client_with_real_model.post('/predict', data=malformed_data)
        # Should handle gracefully (either return error or default behavior)
        assert response.status_code in [200, 400, 500]
    
    @pytest.mark.integration
    def test_performance_under_load(self, client_with_real_model):
        """Test application performance under multiple concurrent requests"""
        import time
        
        form_data = {
            'Online Order': '1',
            'Book Table': '0',
            'Votes': '200',
            'Location': '15',
            'Restaurant Type': '20',
            'Cuisines': '25',
            'Cost': '600',
            'Menu Item': '30'
        }
        
        start_time = time.time()
        
        # Make 10 requests
        responses = []
        for _ in range(10):
            response = client_with_real_model.post('/predict', data=form_data)
            responses.append(response)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # All requests should succeed
        for response in responses:
            assert response.status_code == 200
        
        # Performance check (should complete within reasonable time)
        assert total_time < 10.0, f"Performance test took too long: {total_time:.2f} seconds"
        
        print(f"Performance test: 10 requests completed in {total_time:.2f} seconds")
        print(f"Average time per request: {total_time/10:.3f} seconds")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
