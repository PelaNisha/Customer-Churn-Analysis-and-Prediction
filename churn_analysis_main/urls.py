# yourapp/urls.py
from django.urls import path, re_path
from .views import * 
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path('logout/',CustomLoginView.as_view(), name='logout'),
    path('home/', home, name='home'),
    re_path('generate_report', generate_report, name = 'generate_report'),
    path('churn_models', churn_models, name = 'churn_models'),
    path('predict_churn_data', predict_churn_data, name = 'predict_churn_data'),
    # path('download-predicted-report/', download_predicted_report, name='download_predicted_report'),
    path('download-predicted-data/', download_predicted_data, name='download_predicted_data'),

    #
]
