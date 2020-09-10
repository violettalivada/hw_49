from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from webapp.forms import *


class ProjectListView(ListView):
    template_name = 'project_templates/project_list.html'
    context_object_name = 'projects'
    paginate_by = 2
    paginate_orphans = 0

    def get_queryset(self):
        return Project.objects.all().order_by('-start_date')


class ProjectView(LoginRequiredMixin, DetailView):
    template_name = 'project_templates/project_view.html'
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object
        tasks = project.tasks.order_by('-date')
        context['tasks'] = tasks
        return context


class ProjectCreateView(PermissionRequiredMixin, CreateView):
    model = Project
    template_name = 'project_templates/project_create.html'
    form_class = ProjectForm
    permission_required = 'webapp.add_project'

    def get_success_url(self):
        return reverse('webapp:project_view', kwargs={'pk': self.object.pk})


class ProjectUpdateView(PermissionRequiredMixin, UpdateView):
    model = Project
    template_name = 'project_templates/project_update.html'
    form_class = ProjectForm
    context_key = 'project'
    permission_required = 'webapp.change_project'

    def get_success_url(self):
        return reverse('webapp:project_view', kwargs={'pk': self.object.pk})

    def has_permission(self):
        return super().has_permission() and self.request.user in self.get_object().users.all()


class ProjectDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'project_templates/project_delete.html'
    model = Project
    context_object_name = 'project'
    success_url = reverse_lazy('webapp:index')
    permission_required = 'webapp.delete_project'

    def has_permission(self):
        return super().has_permission() and self.request.user in self.get_object().users.all()


class EditUserView(PermissionRequiredMixin, UpdateView):
    model = Project
    form_class = UserForm
    template_name = 'project_templates/add_users.html'
    permission_required = 'auth.change_user'

    def get_success_url(self):
        return reverse('webapp:project_view', kwargs={'pk': self.object.pk})

    def has_permission(self):
        return super().has_permission() and self.request.user in self.get_object().users.all()




