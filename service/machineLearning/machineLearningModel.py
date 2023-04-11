# * Importing necessary libraries
import pandas as pd
import numpy as np

# * Import Machine Learning Module
from sklearn import preprocessing
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split


# Read the training data from a CSV file
df_training = pd.read_csv("csv_data/Training.csv")

# Split the data into features (X) and labels (y)
X = df_training.iloc[:, :-1]
y = df_training["prognosis"]

# * Separating the features and the target variable
cols = df_training.columns
cols = cols[:-1]

# * Creating a reduced dataset with maximum values of each column for each target class
reduced_data = df_training.groupby(df_training["prognosis"]).max()

# * Converting target variable from string to numbers using LabelEncoder
le = preprocessing.LabelEncoder()
le.fit(y)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# * Create the DecisionTreeClassifier
clf = DecisionTreeClassifier(
    criterion="entropy", max_depth=10, min_samples_leaf=1, min_samples_split=2
)
clf.fit(X_train, y_train)

# Create a dictionary to map symptoms to their indices in the feature vector
symptoms_dict = {symptom: index for index, symptom in enumerate(X.columns)}


# Create an input vector for the given symptoms
input_vector = np.zeros(len(symptoms_dict))
