import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

def final_func(df):
    df['PreferredLoginDevice'] = LabelEncoder().fit_transform(df['PreferredLoginDevice'])
    df['PreferredPaymentMode'] = LabelEncoder().fit_transform(df['PreferredPaymentMode'])
    df['Gender'] = LabelEncoder().fit_transform(df['Gender'])
    df['PreferedOrderCat'] = LabelEncoder().fit_transform(df['PreferedOrderCat'])
    df['MaritalStatus'] = LabelEncoder().fit_transform(df['MaritalStatus'])
    
    # Handling missing values
    df.fillna(df.mean(), inplace=True)

    # Splitting the dataset into features and target variable
    X = df.drop(columns=['Churn'])
    y = df['Churn']

    # Splitting the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Random Forest
    random_forest = RandomForestClassifier()
    random_forest.fit(X_train, y_train)
    churn_predictions = random_forest.predict(X_test)

    # Add test data columns to the results
    test_data_with_predictions = X_test.copy()
    test_data_with_predictions['Predicted Churn'] = churn_predictions

    # Filter rows where predicted churn is 1
    predicted_churn_1 = test_data_with_predictions[test_data_with_predictions['Predicted Churn'] == 1]

    # Return the filtered DataFrame
    print(type(predicted_churn_1))
    return predicted_churn_1