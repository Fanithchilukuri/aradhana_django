# -*- coding: utf-8 -*-
"""ML_predict.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1a1ZPz6TLwFEq_hcy009dM0TGGlEJ7Ui9

# Import necessary libraries
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

"""Load the Dataset"""

data = pd.read_csv('data.csv')

"""Display basic information about the dataset"""

data.info()

"""Display summary statistics"""

print(data.describe())

"""Visualization: Distribution of Wholesale and Retail Costs

"""

plt.figure(figsize=(10, 6))
sns.histplot(data['Wholesale_cost'], kde=True, color='blue', label='Wholesale Cost')
sns.histplot(data['retail_cost'], kde=True, color='green', label='Retail Cost')
plt.title('Distribution of Wholesale and Retail Costs')
plt.xlabel('Cost')
plt.ylabel('Frequency')
plt.legend()
plt.show()

"""Visualization: Profit vs Wholesale Cost"""

plt.figure(figsize=(8, 5))
sns.scatterplot(x='Wholesale_cost', y='profit', data=data, hue='season')
plt.title('Profit vs Wholesale Cost by Season')
plt.xlabel('Wholesale Cost')
plt.ylabel('Profit')
plt.show()



