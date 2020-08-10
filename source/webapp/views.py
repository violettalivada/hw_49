from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.urls import reverse
from django.views.generic import View, TemplateView, FormView
from .forms import *


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tasks = Task.objects.all()
        context['tasks'] = tasks
        return context


class TaskView(TemplateView):
    template_name = 'task_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs.get('pk')
        task = get_object_or_404(Task, pk=pk)

        context['task'] = task
        return context


class TaskCreateView(FormView):
    template_name = 'task_create.html'
    form_class = TaskForm

    def form_valid(self, form):
        data = {}
        types = form.cleaned_data.pop('types')
        for key, value in form.cleaned_data.items():
            if value is not None:
                data[key] = value
        self.task = Task.objects.create(**data)
        self.task.types.set(types)
        return redirect(self.get_redirect_url())

    def get_redirect_url(self):
        return reverse('task_view', kwargs={'pk': self.task.pk})


class TaskUpdateView(FormView):
    template_name = 'task_update.html'
    form_class = TaskForm

    def dispatch(self, request, *args, **kwargs):
        self.task = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = self.task
        return context

    def get_initial(self):
        initial = {}
        for key in 'title', 'description', 'date', 'status':
            initial[key] = getattr(self.task, key)
        initial['type'] = self.task.types.all()
        return initial

    def form_valid(self, form):
        type = form.cleaned_data.pop('types')
        for key, value in form.cleaned_data.items():
            if value is not None:
                setattr(self.task, key, value)
        self.task.save()
        self.task.types.set(type)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('task_view', kwargs={'pk': self.task.pk})

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Task, pk=pk)


class TaskDeleteView(TemplateView):
    template_name = 'task_delete.html'

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




