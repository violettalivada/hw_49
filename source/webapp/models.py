from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator


class Type(models.Model):
    name = models.CharField(max_length=40, verbose_name='Тип')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'


class Status(models.Model):
    name = models.CharField(max_length=40, verbose_name='Статус')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class Task(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False, verbose_name='Заголовок',
                             validators=(MinLengthValidator(10),))
    description = models.TextField(max_length=3000, null=True, blank=True, verbose_name='Описание')
    date = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    update_date = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    types = models.ManyToManyField('webapp.Type', related_name='tasks', blank=True)
    status = models.ForeignKey('webapp.Status', related_name='status', on_delete=models.PROTECT,
                               verbose_name='Статус')
    project = models.ForeignKey('webapp.Project', related_name='tasks', on_delete=models.CASCADE,
                                verbose_name='Проект')

    def __str__(self):
        return "{}. {}".format(self.pk, self.title)

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


class Project(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False, verbose_name='Заголовок')
    description = models.TextField(max_length=3000, null=True, blank=True, verbose_name='Описание')
    start_date = models.DateField(auto_now=False, verbose_name='Дата начала')
    end_date = models.DateField(null=True, blank=True, verbose_name='Дата окончания')
    users = models.ManyToManyField(get_user_model(), related_name='projects', verbose_name='Пользователи')

    def __str__(self):
        return "{}. {}".format(self.pk, self.title)

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
