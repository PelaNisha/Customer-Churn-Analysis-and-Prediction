# Import necessary modules and functions
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
import os
from django.http import HttpResponse
import shutil
from pathlib import Path
import pandas as pd
from .models import Customer, CustomerGroup, ChurnPredictionModel, Transaction



# Import custom functions from scripts
from scripts.save_excel import conv_excel
from scripts.exec_jupyter import final_func
from scripts.prediction import final_func as predict_func
from scripts.prediction_data import final_func as predict_data_func

# Define view for the home page
def home(request):
    return render(request, 'home.html', {'username': request.user.username})

# Custom LoginView to use a custom login template
class CustomLoginView(LoginView):
    template_name = 'login.html'

# View to generate a report
def generate_report(request):
    if request.method == 'POST' and 'get_html' in request.POST:
        # Get the username and uploaded file
        user_ = str(request.user.username)
        my_uploaded_file = request.FILES['file1']
        # Define paths
        path_ = r'\\churn_analysis_main\static\\result\\generate_report\\'
        base_dir = os.path.abspath('.')
        # Create user-specific folder
        user_folder = Path(base_dir + path_ + user_)
        os.makedirs(user_folder, exist_ok=True)
        # Convert uploaded Excel file to HTML
        conv_excel(my_uploaded_file, user_folder)
        # Copy notebook to user folder and execute it
        notebook_path = Path(base_dir + '\\script\\notebooks\\')
        source = str(notebook_path) + "\\generate_report.ipynb"
        destination = str(user_folder) + '\\generate_report.ipynb'
        shutil.copy(source, destination)
        result = final_func(destination, user_)
        # Write result to HTML file
        with open(str(user_folder) + "\\generate_report.html", "w", errors="ignore") as f:
            f.write(result)
        return render(request, 'generate_report.html', {'r': True})
    return render(request, 'generate_report.html')

# View to predict churn using models
def churn_models(request):
    if request.method == 'POST' and 'get_prediction_html' in request.POST:
        # Get the username and uploaded file
        user_ = str(request.user.username)
        my_uploaded_file = request.FILES['file1']
        # Define paths
        path_ = r'\\churn_analysis_main\static\\result\\predict_churn\\'
        base_dir = os.path.abspath('.')
        # Create user-specific folder
        user_folder = Path(base_dir + path_ + user_)
        os.makedirs(user_folder, exist_ok=True)
        # Convert uploaded Excel file to HTML
        conv_excel(my_uploaded_file, user_folder)
        # Predict churn using data
        csv_path = "churn_analysis_main\\static\\result\\predict_churn\\" + user_ + "\\data.xlsx"
        description = pd.read_excel(csv_path, sheet_name='Data Dict')
        data = pd.read_excel(csv_path, sheet_name='E Comm')
        results = predict_func(data)
        return render(request, 'predict_churn.html', {'r': True, 'result_dict': results})
    return render(request, 'predict_churn.html')

# View to predict churn using data
def predict_churn_data(request):
    if request.method == 'POST' and 'get_prediction_data' in request.POST:
        # Get the username and uploaded file
        user_ = str(request.user.username)
        my_uploaded_file = request.FILES['file1']
        # Define paths
        path_ = r'\\churn_analysis_main\static\\result\\predict_churn\\'
        46
        base_dir = os.path.abspath('.')
        # Create user-specific folder
        user_folder = Path(base_dir + path_ + user_)
        os.makedirs(user_folder, exist_ok=True)
        # Convert uploaded Excel file to HTML
        conv_excel(my_uploaded_file, user_folder)
        # Predict churn using data
        csv_path = "churn_analysis_main\\static\\result\\predict_churn\\" + user_ + "\\data.xlsx"
        data = pd.read_excel(csv_path, sheet_name='E Comm')
        results = predict_data_func(data)
        results.to_csv("churn_analysis_main\\static\\result\\predict_churn\\" + user_ + "\\predicted_data.csv", index = False)
        x = results.to_html(classes='table table-striped', index=False)
        return render(request, 'predict_churn_data.html', {'r': True, 'dataframe_html': x})
    return render(request, 'predict_churn_data.html')


# View to download predicted data
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

