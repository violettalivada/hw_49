from webapp.models import Project
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from webapp.forms import *
from django.shortcuts import get_object_or_404, redirect


class ProjectListView(ListView):
    template_name = 'project_templates/project_list.html'
    context_object_name = 'projects'
    paginate_by = 3
    paginate_orphans = 0

    def get_queryset(self):
        return Project.objects.all().order_by('-start_date')


class ProjectView(DetailView):
    template_name = 'project_templates/project_view.html'
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object
        tasks = project.tasks.order_by('-date')
        context['tasks'] = tasks
        return context


class ProjectCreateView(CreateView):
    model = Project
    template_name = 'project_templates/project_create.html'
    form_class = ProjectForm

    def get_success_url(self):
        return reverse('project_view', kwargs={'pk': self.object.pk})


class ProjectUpdateView(UpdateView):
    model = Project
    template_name = 'project_templates/project_update.html'
    form_class = ProjectForm
    context_key = 'project'

    def get_success_url(self):
        return reverse('project_view', kwargs={'pk': self.object.pk})


class ProjectDeleteView(DeleteView):
    template_name = 'project_templates/project_delete.html'
    model = Project
    context_object_name = 'project'
    success_url = reverse_lazy('index')