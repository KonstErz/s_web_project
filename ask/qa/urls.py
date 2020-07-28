from django.urls import path
from . import views


urlpatterns = [
    path('', views.question_list, name='question_list'),
    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('question/<int:pk>/', views.question_details, name='question_details'),
    path('ask/', views.ask, name='ask'),
    path('popular/', views.popular, name='popular'),
    path('like/', views.like_question, name='like_question'),
]
