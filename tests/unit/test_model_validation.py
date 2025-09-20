"""
Unit tests for model validation and functionality
"""
import pytest
import pandas as pd
import numpy as np
import pickle
import os
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.ensemble import ExtraTreesRegressor


class TestModelValidation:
    """Test class for model validation and performance metrics"""
    
    @pytest.fixture
    def model(self):
        """Load the trained model"""
        if not os.path.exists('../model.pkl'):
            pytest.skip("Model file 'model.pkl' not found. Run model.py first.")
        
        with open('../model.pkl', 'rb') as f:
            model = pickle.load(f)
        return model
    
    @pytest.fixture
    def test_data(self):
        """Load and prepare test data"""
        if not os.path.exists('../zomato_df.csv'):
            pytest.skip("Dataset 'zomato_df.csv' not found.")
        
        df = pd.read_csv('../zomato_df.csv')
        if 'Unnamed: 0' in df.columns:
            df.drop('Unnamed: 0', axis=1, inplace=True)
        
        # Prepare features and target
        X = df.drop('rate', axis=1)
        y = df['rate']
        
        return X, y
    
    @pytest.mark.unit
    def test_model_type(self, model):
        """Test that the model is of the expected type"""
        assert isinstance(model, ExtraTreesRegressor), \
            f"Expected ExtraTreesRegressor, got {type(model)}"
    
    @pytest.mark.unit
    def test_model_parameters(self, model):
        """Test that the model has expected parameters"""
        assert hasattr(model, 'n_estimators'), "Model missing n_estimators parameter"
        assert model.n_estimators == 120, f"Expected 120 estimators, got {model.n_estimators}"
    
    @pytest.mark.unit
    def test_model_is_fitted(self, model):
        """Test that the model is properly fitted"""
        assert hasattr(model, 'feature_importances_'), "Model is not fitted"
        assert len(model.feature_importances_) > 0, "Model has no feature importances"
    
    @pytest.mark.unit
    def test_model_prediction_output_type(self, model, test_data):
        """Test that model predictions are of correct type and shape"""
        X, y = test_data
        
        # Test with a small sample
        X_sample = X.head(10)
        predictions = model.predict(X_sample)
        
        assert isinstance(predictions, np.ndarray), "Predictions should be numpy array"
        assert len(predictions) == len(X_sample), "Number of predictions should match input size"
        assert all(isinstance(pred, (int, float, np.number)) for pred in predictions), \
            "All predictions should be numeric"
    
    @pytest.mark.unit
    def test_model_prediction_range(self, model, test_data):
        """Test that model predictions are within reasonable range"""
        X, y = test_data
        
        # Test with a sample
        X_sample = X.head(100)
        predictions = model.predict(X_sample)
        
        # Ratings should typically be between 0 and 5
        assert all(0 <= pred <= 5 for pred in predictions), \
            f"Some predictions are outside [0, 5] range: {predictions}"
    
    @pytest.mark.unit
    def test_model_performance_metrics(self, model, test_data):
        """Test model performance with basic metrics"""
        X, y = test_data
        
        # Split data for testing (using same random state as training)
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=10
        )
        
        # Make predictions
        y_pred = model.predict(X_test)
        
        # Calculate metrics
        mse = mean_squared_error(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        # Basic performance checks
        assert mse >= 0, f"MSE should be non-negative, got {mse}"
        assert mae >= 0, f"MAE should be non-negative, got {mae}"
        assert -1 <= r2 <= 1, f"R² should be between -1 and 1, got {r2}"
        
        # Performance thresholds (adjust based on your expectations)
        assert r2 > 0.5, f"R² score {r2:.3f} is too low, expected > 0.5"
        assert mae < 1.0, f"MAE {mae:.3f} is too high, expected < 1.0"
        
        print(f"\nModel Performance Metrics:")
        print(f"MSE: {mse:.3f}")
        print(f"MAE: {mae:.3f}")
        print(f"R²: {r2:.3f}")
    
    @pytest.mark.unit
    def test_feature_importance(self, model):
        """Test that feature importances are available and reasonable"""
        importances = model.feature_importances_
        
        assert len(importances) > 0, "No feature importances available"
        assert all(imp >= 0 for imp in importances), "Feature importances should be non-negative"
        assert abs(sum(importances) - 1.0) < 1e-6, "Feature importances should sum to 1"
        
        # Check that at least some features have significant importance
        max_importance = max(importances)
        assert max_importance > 0.01, "No features have significant importance"
        
        print(f"\nTop 5 Most Important Features:")
        # This would need feature names to be more meaningful
        top_indices = np.argsort(importances)[-5:][::-1]
        for i, idx in enumerate(top_indices):
            print(f"{i+1}. Feature {idx}: {importances[idx]:.3f}")


class TestDataQuality:
    """Test class for data quality and preprocessing validation"""
    
    @pytest.fixture
    def dataset(self):
        """Load the dataset"""
        if not os.path.exists('../zomato_df.csv'):
            pytest.skip("Dataset 'zomato_df.csv' not found.")
        
        df = pd.read_csv('../zomato_df.csv')
        if 'Unnamed: 0' in df.columns:
            df.drop('Unnamed: 0', axis=1, inplace=True)
        
        return df
    
    @pytest.mark.unit
    def test_dataset_shape(self, dataset):
        """Test that dataset has expected shape"""
        assert len(dataset) > 0, "Dataset is empty"
        assert len(dataset.columns) >= 8, f"Expected at least 8 columns, got {len(dataset.columns)}"
        
        print(f"Dataset shape: {dataset.shape}")
    
    @pytest.mark.unit
    def test_target_variable(self, dataset):
        """Test that target variable (rate) exists and is valid"""
        assert 'rate' in dataset.columns, "Target variable 'rate' not found"
        
        rates = dataset['rate']
        assert not rates.isnull().all(), "All rate values are null"
        assert rates.dtype in ['int64', 'float64'], f"Rate column has unexpected dtype: {rates.dtype}"
        
        # Check rate range
        assert rates.min() >= 0, f"Minimum rate {rates.min()} is negative"
        assert rates.max() <= 5, f"Maximum rate {rates.max()} exceeds 5"
        
        print(f"Rate statistics:")
        print(f"Min: {rates.min()}")
        print(f"Max: {rates.max()}")
        print(f"Mean: {rates.mean():.2f}")
        print(f"Std: {rates.std():.2f}")
    
    @pytest.mark.unit
    def test_feature_variables(self, dataset):
        """Test that feature variables are valid"""
        features = dataset.drop('rate', axis=1)
        
        for col in features.columns:
            assert not features[col].isnull().all(), f"All values in {col} are null"
            
            # Check for reasonable data types
            if features[col].dtype == 'object':
                print(f"Warning: {col} is object type, consider encoding")
    
    @pytest.mark.unit
    def test_no_infinite_values(self, dataset):
        """Test that dataset contains no infinite values"""
        numeric_cols = dataset.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            assert not np.isinf(dataset[col]).any(), f"Column {col} contains infinite values"
    
    @pytest.mark.unit
    def test_data_consistency(self, dataset):
        """Test data consistency and basic sanity checks"""
        # Check that online_order and book_table are binary (0 or 1)
        if 'online_order' in dataset.columns:
            online_order_values = set(dataset['online_order'].unique())
            assert online_order_values.issubset({0, 1}), \
                f"online_order contains unexpected values: {online_order_values}"
        
        if 'book_table' in dataset.columns:
            book_table_values = set(dataset['book_table'].unique())
            assert book_table_values.issubset({0, 1}), \
                f"book_table contains unexpected values: {book_table_values}"
        
        # Check that votes are non-negative
        if 'votes' in dataset.columns:
            assert (dataset['votes'] >= 0).all(), "Votes contain negative values"
        
        # Check that cost is positive
        if 'cost' in dataset.columns:
            assert (dataset['cost'] > 0).all(), "Cost contains non-positive values"


class TestModelRobustness:
    """Test class for model robustness and edge cases"""
    
    @pytest.fixture
    def model(self):
        """Load the trained model"""
        if not os.path.exists('../model.pkl'):
            pytest.skip("Model file 'model.pkl' not found. Run model.py first.")
        
        with open('../model.pkl', 'rb') as f:
            model = pickle.load(f)
        return model
    
    @pytest.mark.unit
    def test_model_with_edge_case_inputs(self, model):
        """Test model behavior with edge case inputs"""
        # Test with minimum values
        min_input = np.array([[0, 0, 0, 0, 0, 0, 1, 0]])
        min_prediction = model.predict(min_input)
        assert len(min_prediction) == 1
        assert 0 <= min_prediction[0] <= 5
        
        # Test with maximum values (assuming reasonable ranges)
        max_input = np.array([[1, 1, 10000, 100, 100, 100, 5000, 100]])
        max_prediction = model.predict(max_input)
        assert len(max_prediction) == 1
        assert 0 <= max_prediction[0] <= 5
    
    @pytest.mark.unit
    def test_model_with_single_feature_variation(self, model):
        """Test how model responds to changes in individual features"""
        base_input = np.array([[1, 0, 100, 5, 10, 15, 500, 20]])
        base_prediction = model.predict(base_input)[0]
        
        # Test online_order variation
        online_order_input = np.array([[0, 0, 100, 5, 10, 15, 500, 20]])
        online_order_prediction = model.predict(online_order_input)[0]
        
        # Test book_table variation
        book_table_input = np.array([[1, 1, 100, 5, 10, 15, 500, 20]])
        book_table_prediction = model.predict(book_table_input)[0]
        
        # Predictions should be different (model should be sensitive to input changes)
        assert abs(base_prediction - online_order_prediction) > 0.01, \
            "Model not sensitive to online_order changes"
        assert abs(base_prediction - book_table_prediction) > 0.01, \
            "Model not sensitive to book_table changes"
    
    @pytest.mark.unit
    def test_model_prediction_consistency(self, model):
        """Test that model gives consistent predictions for same input"""
        test_input = np.array([[1, 0, 100, 5, 10, 15, 500, 20]])
        
        predictions = []
        for _ in range(5):
            pred = model.predict(test_input)[0]
            predictions.append(pred)
        
        # All predictions should be identical (deterministic model)
        assert all(abs(p - predictions[0]) < 1e-10 for p in predictions), \
            "Model predictions are not consistent"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
