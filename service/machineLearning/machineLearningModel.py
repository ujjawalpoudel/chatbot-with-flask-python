# * Importing necessary libraries
import pandas as pd
import numpy as np

# * Import Machine Learning Module
from sklearn import preprocessing
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split


# * Loading training and testing data
training = pd.read_csv("csv_data/Training.csv")
testing = pd.read_csv("csv_data/Testing.csv")

# * Separating the features and the target variable
cols = training.columns
cols = cols[:-1]
x = training[cols]
y = training["prognosis"]

# * Creating a reduced dataset with maximum values of each column for each target class
reduced_data = training.groupby(training["prognosis"]).max()

# * Converting target variable from string to numbers using LabelEncoder
le = preprocessing.LabelEncoder()
le.fit(y)
y = le.transform(y)

# * Splitting the data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.33, random_state=42
)

# * Create the DecisionTreeClassifier
clf = DecisionTreeClassifier(
    criterion="entropy", max_depth=10, min_samples_leaf=1, min_samples_split=2
)
clf.fit(x_train, y_train)

model = SVC()
model.fit(x_train, y_train)

# * Getting feature importances and indices of features in descending order
importances = clf.feature_importances_
indices = np.argsort(importances)[::-1]
features = cols

symptoms_dict = {symptom: index for index, symptom in enumerate(x)}
input_vector = np.zeros(len(symptoms_dict))
