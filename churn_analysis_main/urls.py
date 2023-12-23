# yourapp/urls.py
from django.urls import path
from .views import * 

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path('home/', home, name='home'),
    path('generate_report', generate_report, name = 'generate_report'),
    path('predict_churn', predict_churn, name = 'predict_churn')
]
