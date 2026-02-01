"""
URL configuration for Session A/B Learning System
"""
from django.urls import path
from . import views

urlpatterns = [
    # Main Screen
    path('main-screen/', views.main_screen, name='main-screen'),

    # Session Management
    path('start/', views.start_session, name='start-session'),
    path('complete/', views.complete_session, name='complete-session'),
    path('step/<int:session_id>/', views.get_step_data, name='get-step-data'),

    # Step Submission
    path('submit/step-1/', views.submit_step_1, name='submit-step-1'),
    path('submit/step-2/', views.submit_step_2, name='submit-step-2'),
    path('submit/step-3/', views.submit_step_3, name='submit-step-3'),
    path('submit/step-4/', views.submit_step_4, name='submit-step-4'),
    path('submit/step-5/', views.submit_step_5, name='submit-step-5'),
]
