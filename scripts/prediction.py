import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

import sys

# Load the dataset      

def final_func(file_):
    df = file_

    # Preprocessing
    df['PreferredLoginDevice'] = LabelEncoder().fit_transform(df['PreferredLoginDevice'])
    df['PreferredPaymentMode'] = LabelEncoder().fit_transform(df['PreferredPaymentMode'])
    df['Gender'] = LabelEncoder().fit_transform(df['Gender'])
    df['PreferedOrderCat'] = LabelEncoder().fit_transform(df['PreferedOrderCat'])
    df['MaritalStatus'] = LabelEncoder().fit_transform(df['MaritalStatus'])

    # Handling missing values
    df.fillna(df.mean(), inplace=True)

    # Splitting the dataset into features and target variable
    X = df.drop(columns=['CustomerID', 'Churn'])
    y = df['Churn']

    # Splitting the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)



    # Logistic Regression
    log_reg = LogisticRegression()
    log_reg.fit(X_train, y_train)
    log_reg_pred = log_reg.predict(X_test)
    # Initialize classifiers
    classifiers = {
        "Logistic Regression": LogisticRegression(),
        "Decision Tree": DecisionTreeClassifier(),
        "Random Forest": RandomForestClassifier()
    }

    results = {}

    # Iterate through each classifier
    for clf_name, clf in classifiers.items():
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, output_dict=True)
        results[clf_name] = {"Accuracy": accuracy, "Classification Report": report}
        
    # Print the results in a formatted way
    for clf_name, result in results.items():
        for key, value in result["Classification Report"].items():
            if isinstance(value, dict):  # If it's a nested dictionary
                for sub_key, sub_value in value.items():
                    pass
            else:
                pass
    return results