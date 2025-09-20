
import pandas as pd
import numpy as np
import sklearn
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.model_selection import train_test_split
import os

import warnings
warnings.filterwarnings('ignore')

# Check if dataset exists, if not create dummy data
if os.path.exists('zomato_df.csv'):
    df = pd.read_csv('zomato_df.csv')
    print("Using existing dataset")
else:
    print("Dataset not found, creating dummy data for model training...")
    # Create dummy dataset with same structure
    np.random.seed(42)
    n_samples = 1000
    
    data = {
        'online_order': np.random.randint(0, 2, n_samples),
        'book_table': np.random.randint(0, 2, n_samples),
        'rate': np.random.uniform(2.0, 5.0, n_samples),
        'votes': np.random.randint(10, 1000, n_samples),
        'location': np.random.randint(1, 100, n_samples),
        'rest_type': np.random.randint(1, 100, n_samples),
        'cuisines': np.random.randint(1, 200, n_samples),
        'cost': np.random.randint(100, 2000, n_samples),
        'menu_item': np.random.randint(1, 100, n_samples)
    }
    
    df = pd.DataFrame(data)
    print("Dummy dataset created")

# Drop 'Unnamed: 0' column if it exists
if 'Unnamed: 0' in df.columns:
    df.drop('Unnamed: 0', axis=1, inplace=True)

print(df.head())
x=df.drop('rate',axis=1)
y=df['rate']
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=.3,random_state=10)


#Preparing Extra Tree Regression
from sklearn.ensemble import  ExtraTreesRegressor
ET_Model=ExtraTreesRegressor(n_estimators = 120)
ET_Model.fit(x_train,y_train)


y_predict=ET_Model.predict(x_test)


import pickle
# # Saving model to disk
pickle.dump(ET_Model, open('model.pkl','wb'))
model=pickle.load(open('model.pkl','rb'))
print(y_predict)
