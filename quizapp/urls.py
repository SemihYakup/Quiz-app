from django.urls import path
from . import views

app_name = 'quizapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('quiz/<int:pk>/', views.quiz_detail, name='quiz_detail'),
    path('quiz/<int:pk>/submit/', views.quiz_submit, name='quiz_submit'),
    path('my-quizzes/', views.my_quizzes, name='my_quizzes'),
    path('create/', views.create_quiz, name='create_quiz'),
    path('quiz/<int:pk>/add-question/', views.add_question, name='add_question'),
    path('quiz/<int:quiz_pk>/delete-question/<int:question_pk>/', views.delete_question, name='delete_question'),
    path('quiz/<int:pk>/delete/', views.delete_quiz, name='delete_quiz'),
]