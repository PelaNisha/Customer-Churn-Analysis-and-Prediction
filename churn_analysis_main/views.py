# Import necessary modules
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
import os
from django.http import HttpResponse
import shutil
from pathlib import Path
import pandas as pd
from scripts.save_excel import conv_excel
from scripts.exec_jupyter import final_func
from scripts.prediction import final_func as predict_func
from scripts.prediction_data import final_func as predict_data_func

# Render the home page
def home(request):
    return render(request, 'home.html', {'username': request.user.username})

# Custom login view
class CustomLoginView(LoginView):
    template_name = 'login.html'

# Generate report view
def generate_report(request):
    if request.method == 'POST' and 'get_html' in request.POST:
        # Get the current user
        user_ = str(request.user.username)
        
        # Get the uploaded file
        my_uploaded_file = request.FILES['file1']
        
        # Define the path
        path_ = r'\\churn_analysis_main\static\\result\\generate_report\\'
        base_dir = os.path.abspath('.')
        
        # Create user folder
        user_folder = Path(base_dir + path_ + user_)
        os.makedirs(user_folder, exist_ok=True)
        
        # Convert uploaded file to excel
        conv_excel(my_uploaded_file, user_folder)
        
        # Copy notebook
        notebook_path = Path(base_dir + '\\script\\notebooks\\')
        source = str(notebook_path) + "\\generate_report.ipynb"
        destination = str(user_folder) + '\\generate_report.ipynb'
        shutil.copy(source, destination)
        
        # Execute notebook and get result
        result = final_func(destination, user_)
        
        # Write result to HTML file
        with open(str(user_folder) + "\\generate_report.html", "w", errors="ignore") as f:
            f.write(result)
            
        # Render the page with the result
        return render(request, 'generate_report.html', {'r': True})

    return render(request, 'generate_report.html')

# Churn models view
def churn_models(request):
    if request.method == 'POST' and 'get_prediction_html' in request.POST:
        # Get the current user
        user_ = str(request.user.username)
        
        # Get the uploaded file
        my_uploaded_file = request.FILES['file1']
        
        # Define the path
        path_ = r'\\churn_analysis_main\static\\result\\predict_churn\\'
        base_dir = os.path.abspath('.')
        
        # Create user folder
        user_folder = Path(base_dir + path_ + user_)
        os.makedirs(user_folder, exist_ok=True)
        
        # Convert uploaded file to excel
        conv_excel(my_uploaded_file, user_folder)
        
        # Read data from excel
        csv_path = "churn_analysis_main\\static\\result\\predict_churn\\" + user_ + "\\data.xlsx"
        description = pd.read_excel(csv_path, sheet_name='Data Dict')
        data = pd.read_excel(csv_path, sheet_name='E Comm')
        
        # Predict churn
        results = predict_func(data)

        # Render the page with the result
        return render(request, 'predict_churn.html', {'r': True, 'result_dict': results})

    return render(request, 'predict_churn.html')

# Predict churn data view
def predict_churn_data(request):
    if request.method == 'POST' and 'get_prediction_data' in request.POST:
        # Get the current user
        user_ = str(request.user.username)
        
        # Get the uploaded file
        my_uploaded_file = request.FILES['file1']
        
        # Define the path
        path_ = r'\\churn_analysis_main\static\\result\\predict_churn\\'
        base_dir = os.path.abspath('.')
        
        # Create user folder
        user_folder = Path(base_dir + path_ + user_)
        os.makedirs(user_folder, exist_ok=True)
        
        # Convert uploaded file to excel
        conv_excel(my_uploaded_file, user_folder)
        
        # Read data from excel
        csv_path = "churn_analysis_main\\static\\result\\predict_churn\\" + user_ + "\\data.xlsx"
        description = pd.read_excel(csv_path, sheet_name='Data Dict')
        data = pd.read_excel(csv_path, sheet_name='E Comm')
        
        # Predict churn
        results = predict_data_func(data)
        
        # Convert prediction result to HTML table
        x = results.to_html(classes='table table-striped', index=False)
        
        # Write prediction result to CSV file
        loc = "churn_analysis_main\\static\\result\\predict_churn\\"+ user_ + "\\predicted_data.csv"
        csv_data = results.to_csv(loc, index=False)
        
        # Render the page with the prediction result
        return render(request, 'predict_churn_data.html', {'r': True, 'dataframe_html': x})

    return render(request, 'predict_churn_data.html')

# Download predicted data view
def download_predicted_data(request):
    # Path to the CSV file
    file_path = os.path.join('churn_analysis_main', 'static', 'result', 'predict_churn', request.user.username, 'predicted_data.csv')
    
    # Open the file in binary mode for reading
    with open(file_path, 'rb') as f:
        # Create an HTTP response with the CSV file as content
        response = HttpResponse(f.read(), content_type='text/csv')
        # Set the file name for download
        response['Content-Disposition'] = 'attachment; filename="predicted_data.csv"'
    
    return response
