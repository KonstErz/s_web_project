from django.urls import path
from . import views


urlpatterns = [
    path('', views.question_list, name='question_list'),
    path('login/', views.test, name='login'),
    path('signup/', views.test, name='signup'),
    path('question/<int:pk>/', views.question_details, name='question_details'),
    path('ask/', views.ask, name='ask'),
    path('popular/', views.popular, name='popular'),
]
