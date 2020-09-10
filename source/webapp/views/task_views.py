from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from webapp.models import *
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, UpdateView, ListView, CreateView, DeleteView, DetailView
from webapp.forms import *
from django.db.models import Q


class IndexView(ListView):
    template_name = 'task_templates/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 3
    paginate_orphans = 0

    def get_queryset(self):
        data = Task.objects.all()
        form = SimpleSearchForm(data=self.request.GET)
        if form.is_valid():
            search = form.cleaned_data['search']
            if search:
                data = data.filter(Q(title__icontains=search) | Q(description__icontains=search))
        return data.order_by('-date')


class TaskView(PermissionRequiredMixin, DetailView):
    template_name = 'task_templates/task_view.html'
    model = Task
    permission_required = 'webapp.view_task'

    def has_permission(self):
        return super().has_permission() and self.request.user in self.get_object().project.users.all()


class TaskCreateView(PermissionRequiredMixin, CreateView):
    model = Task
    template_name = 'task_templates/task_create.html'
    form_class = TaskForm
    permission_required = 'webapp.add_task'

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        task = form.save(commit=False)
        task.project = project
        task.save()
        form.save_m2m()
        return redirect('webapp:project_view', pk=project.pk)

    def has_permission(self):
        return super().has_permission() and self.request.user in self.get_object().project.users.all()


class TaskUpdateView(PermissionRequiredMixin, UpdateView):
    model = Task
    template_name = 'task_templates/task_update.html'
    form_class = TaskForm
    context_object_name = 'task'
    permission_required = 'webapp.change_task'

    def get_success_url(self):
        return reverse('webapp:task_view', kwargs={'pk': self.object.pk})

    def has_permission(self):
        return super().has_permission() and self.request.user in self.get_object().project.users.all()


class TaskDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'task_templates/task_delete.html'
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('webapp:index')
    permission_required = 'webapp.delete_task'

    def has_permission(self):
        return super().has_permission() and self.request.user in self.get_object().project.users.all()





