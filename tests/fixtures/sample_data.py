"""
Sample data fixtures for testing
"""
import numpy as np
import pandas as pd


def get_sample_restaurant_data():
    """Get sample restaurant data for testing"""
    return {
        'online_order': [1, 0, 1, 0, 1],
        'book_table': [1, 0, 0, 1, 0],
        'votes': [775, 787, 918, 88, 166],
        'location': [20, 20, 16, 62, 20],
        'rest_type': [20, 20, 16, 62, 20],
        'cuisines': [1386, 594, 484, 1587, 1406],
        'cost': [800.0, 800.0, 800.0, 300.0, 600.0],
        'menu_item': [5047, 5047, 5047, 5047, 5047],
        'rate': [4.1, 4.1, 3.8, 3.7, 3.8]
    }


def get_sample_form_data():
    """Get sample form data for testing"""
    return {
        'Online Order': '1',
        'Book Table': '0',
        'Votes': '100',
        'Location': '5',
        'Restaurant Type': '10',
        'Cuisines': '15',
        'Cost': '500',
        'Menu Item': '20'
    }


def get_edge_case_data():
    """Get edge case data for testing"""
    return {
        'min_values': [0, 0, 0, 0, 0, 0, 1, 0],
        'max_values': [1, 1, 10000, 100, 100, 100, 5000, 100],
        'mixed_values': [1, 0, 500, 25, 30, 45, 800, 60]
    }


def get_invalid_data():
    """Get invalid data for testing error handling"""
    return {
        'non_numeric': ['invalid', 'not_a_number', 'also_invalid', '5', '10', '15', '500', '20'],
        'negative_values': [-1, -5, -100, -5, -10, -15, -500, -20],
        'out_of_range': [2, 2, 100000, 1000, 1000, 1000, 100000, 1000]
    }


def create_sample_dataframe():
    """Create a sample DataFrame for testing"""
    data = get_sample_restaurant_data()
    df = pd.DataFrame(data)
    return df


def get_expected_feature_names():
    """Get expected feature names"""
    return [
        'Online Order', 'Book Table', 'Votes', 'Location',
        'Restaurant Type', 'Cuisines', 'Cost', 'Menu Item'
    ]


def get_expected_rating_range():
    """Get expected rating range"""
    return (0, 5)


def get_performance_test_data():
    """Get data for performance testing"""
    return {
        'high_end_restaurant': {
            'Online Order': '1',
            'Book Table': '1',
            'Votes': '1000',
            'Location': '50',
            'Restaurant Type': '40',
            'Cuisines': '60',
            'Cost': '2000',
            'Menu Item': '80'
        },
        'budget_restaurant': {
            'Online Order': '0',
            'Book Table': '0',
            'Votes': '50',
            'Location': '10',
            'Restaurant Type': '5',
            'Cuisines': '10',
            'Cost': '200',
            'Menu Item': '15'
        },
        'mid_range_restaurant': {
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
