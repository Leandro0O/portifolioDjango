from django.urls import path
from . import views

app_name = 'project'

urlpatterns = [
    path('', views.Home, name='home'),
    path('contato/', views.Email,name='email'),
    path('<slug:slug>/', views.ProjectDetailView.as_view(),name='detail'),
    
    
]