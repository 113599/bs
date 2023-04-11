import app.views

from django.urls import path

urlpatterns = [
    path('<str:module>/', app.views.SysView.as_view()),
    path('notices/<str:module>/', app.views.NoticesView.as_view()),
    path('colleges/<str:module>/', app.views.CollegesView.as_view()),
    path('grades/<str:module>/', app.views.GradesView.as_view()),
    path('projects/<str:module>/', app.views.ProjectsView.as_view()),
    path('students/<str:module>/', app.views.StudentsView.as_view()),
    path('teachers/<str:module>/', app.views.TeachersView.as_view()),
    path('works/<str:module>/', app.views.WorksView.as_view()),
    path('checks/<str:module>/', app.views.ChecksView.as_view()),
    path('checklogs/<str:module>/', app.views.CheckLogsView.as_view()),
    path('leaves/<str:module>/', app.views.LeaveLogsView.as_view()),
]