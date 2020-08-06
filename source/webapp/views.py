from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.views.generic import View, TemplateView
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


class TaskCreateView(View):
    def get(self, request):
        form = TaskForm()
        return render(request, 'task_create.html', context={
            'form': form
        })

    def post(self, request):
        form = TaskForm(data=request.POST)
        if form.is_valid():
            data = {}
            for key, value in form.cleaned_data.items():
                if value is not None:
                    data[key] = value
            task = Task.objects.create(**data)
            return redirect('task_view', pk=task.pk)
        else:
            return render(request, 'task_create.html', context={
                'form': form
            })


class TaskUpdateView(TemplateView):
    template_name = 'task_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs.get('pk')
        task = get_object_or_404(Task, pk=pk)

        initial = {}
        for key in 'title', 'description', 'date', 'type', 'status':
            initial[key] = getattr(task, key)
        form = TaskForm(initial=initial)

        context['task'] = task
        context['form'] = form

        return context

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        form = TaskForm(data=request.POST)
        if form.is_valid():
            for key, value in form.cleaned_data.items():
                if value is not None:
                    setattr(task, key, value)
            task.save()
            return redirect('task_view', pk=task.pk)
        else:
            return self.render_to_response({
                'task': task,
                'form': form
            })


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




