# yourapp/views.py
from django.contrib.auth.views import LoginView
from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import user_passes_test
import os
import sys
import shutil 
from pathlib import Path

def home(request):
    return render(request, 'home.html', {'username': request.user.username})

class CustomLoginView(LoginView):
    template_name = 'login.html'
    # success_url =  reverse_lazy('home')

# def predict_churn(request):
#     return render(request, 'predict_churn.html')

def generate_report(request):
    if request.method =='POST' and'get_html' in request.POST:
            user_ = str(request.user.username)
            my_uploaded_file = request.FILES['file1']	
            print("file uploaded")
            
            path_ = r'\\churn_analysis_main\static\\result\\generate_report\\'
            base_dir = os.path.abspath('.')
            print("apth is ", Path(base_dir+ path_ + str(request.user.username)+'\\'))
            try:
                user_folder = Path(base_dir+ path_ + str(request.user.username)+'\\')
            
            except:
                os.makedirs(Path(base_dir+ path_ + str(request.user.username)+'\\'))
                print('except case ')
            notebook_path = Path(base_dir+'\\script\\notebooks\\')
            print('notebook path ', notebook_path)
            if os.path.exists(user_folder):
                filelist = [ f for f in os.listdir(user_folder) ]
                for f in filelist:
                    os.remove(Path(user_folder, f))
            if not os.path.exists(user_folder):
                os.makedirs(user_folder)
            print('user folder ', user_folder)
            sys.path.append('..')
            print("now function calling")
            from scripts.save_excel import conv_excel
            print("-------")
            # print()
            conv_excel(my_uploaded_file,user_folder)
        

            from scripts.exec_jupyter import final_func
            source = str(notebook_path) + "\\generate_report.ipynb"
            destination  = str(user_folder)+'\\generate_report.ipynb'
            shutil.copy(source, destination)
            result = final_func(destination,user_)
            with open(str(user_folder) +"\\generate_report.html", "w", errors="ignore") as f:
                f.write(result)
            return render(request, 'generate_report.html',{'r':True})

    return render(request, 'generate_report.html')

# @user_passes_test(lambda u: u.groups.filter(name__in=['Normal', 'Admin', 'Viewer']).exists(), login_url='logout')
def predict_churn(request):
    if request.method =='POST' and'get_html' in request.POST:
            selected_dropdown_option = request.POST['dropdown'] 
            user_ = str(request.user.username)
            my_uploaded_file = request.FILES['file1']	
            base_dir = os.path.abspath('.')
            path_ = r'\\main\\static\\result\\predict_churn\\'
            try:
                user_folder = os.path.join(base_dir+ path_ + str(request.user.username)+'/')
            except:
                os.makedirs(os.path.join(base_dir+ path_ + str(request.user.username)+'/'))
            notebook_path = os.path.join(base_dir+'/script/notebooks/')

            if os.path.exists(user_folder):
                filelist = [ f for f in os.listdir(user_folder) ]
                for f in filelist:
                    os.remove(os.path.join(user_folder, f))
            if not os.path.exists(user_folder):
                os.makedirs(user_folder)
            
            sys.path.append('..')
            
            from churn_analysis.scripts.save_excel import conv_csv
            conv_csv(my_uploaded_file,user_folder)
        

            from scripts.exec_jupyter import final_func
            source = notebook_path + "predict_churn.ipynb"
            destination  = user_folder+'predict_churn.ipynb'
            shutil.copy(source, destination)
            P = int(request.POST.get('P'))
            
            if selected_dropdown_option == 'Percentage':
                result = final_func(destination, user_, P,  0)

            elif selected_dropdown_option == 'Target':
                result = final_func(destination,user_, 0,  P)
                
            with open(user_folder +"predict_churn.html", "w") as f:
                f.write(result)

            return render(request, 'predict_churn.html',{'r':True})

    return render(request, 'predict_churn.html')