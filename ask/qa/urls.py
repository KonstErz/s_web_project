from django.urls import path
from . import views


urlpatterns = [
    path('', views.test, name='question_list'),
    path('login/', views.test, name='login'),
    path('signup/', views.test, name='signup'),
    path('question/<int:pk>/', views.test, name='question_detail'),
    path('ask/', views.test, name='ask'),
    path('popular/', views.test, name='popular'),
    path('new/', views.test, name='new'),
]
