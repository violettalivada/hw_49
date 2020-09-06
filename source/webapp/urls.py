from django.urls import path
from webapp.views import *


app_name = 'webapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('task/<int:pk>/', TaskView.as_view(), name='task_view'),
    path('task/<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
    path('projects/', ProjectListView.as_view(), name='project_list'),
    path('project/<int:pk>/', ProjectView.as_view(), name='project_view'),
    path('project/<int:pk>/tasks/add', TaskCreateView.as_view(), name='task_create'),
    path('projects/add/', ProjectCreateView.as_view(), name='project_create'),
    path('project/<int:pk>/update/', ProjectUpdateView.as_view(), name='project_update'),
    path('project/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project_delete'),
]