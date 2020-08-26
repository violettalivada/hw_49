from django.shortcuts import redirect, get_object_or_404
from webapp.models import *
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, UpdateView, ListView, CreateView, DeleteView
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


class TaskView(TemplateView):
    template_name = 'task_templates/task_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        task = get_object_or_404(Task, pk=pk)
        context['task'] = task
        return context


class TaskCreateView(CreateView):
    model = Task
    template_name = 'task_templates/task_create.html'
    form_class = TaskForm

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        task = form.save(commit=False)
        task.project = project
        task.save()
        form.save_m2m()
        return redirect('project_view', pk=project.pk)


class TaskUpdateView(UpdateView):
    model = Task
    template_name = 'task_templates/task_update.html'
    form_class = TaskForm
    context_object_name = 'task'

    def get_success_url(self):
        return reverse('task_view', kwargs={'pk': self.object.pk})


class TaskDeleteView(DeleteView):
    template_name = 'task_templates/task_delete.html'
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('index')



