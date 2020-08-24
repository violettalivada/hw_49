from django.shortcuts import redirect, get_object_or_404
from .models import *
from django.urls import reverse
from django.views.generic import TemplateView, FormView, ListView
from .forms import *
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


class TaskCreateView(FormView):
    template_name = 'task_templates/task_create.html'
    form_class = TaskForm

    def form_valid(self, form):
        self.task = form.save()
        return redirect(self.get_redirect_url())

    def get_redirect_url(self):
        return reverse('task_view', kwargs={'pk': self.task.pk})


class TaskUpdateView(FormView):
    template_name = 'task_templates/task_update.html'
    form_class = TaskForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.task
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        self.task = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = self.task
        return context

    def form_valid(self, form):
        self.task = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('task_view', kwargs={'pk': self.task.pk})

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Task, pk=pk)


class TaskDeleteView(TemplateView):
    template_name = 'task_templates/task_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        task = get_object_or_404(Task, pk=pk)

        context['task'] = task
        return context

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.delete()
        return redirect('index')




