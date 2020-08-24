from django.shortcuts import redirect, get_object_or_404
from webapp.models import *
from django.urls import reverse
from django.views.generic import TemplateView, FormView, ListView
from webapp.forms import *
from django.db.models import Q


class ProjectListView(ListView):
    template_name = 'project_templates/project_list.html'
    context_object_name = 'projects'
    paginate_by = 3
    paginate_orphans = 0

    def get_queryset(self):
        return Project.objects.all().order_by('-start_date')
