# yourapp/urls.py
from django.urls import path, re_path
from .views import * 
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    path('home/', home, name='home'),
    re_path('generate_report', generate_report, name = 'generate_report'),
    path('predict_churn', predict_churn, name = 'predict_churn'),
]
