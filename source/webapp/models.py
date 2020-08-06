from django.db import models


TYPE_CHOICES = [
    ('task', 'Задача'),
    ('bug', 'Ошибка'),
    ('enhancement', 'Улучшение')
]

STATUS_CHOICES = [
    ('new', 'Новый'),
    ('in_progress', 'В процессе'),
    ('done', 'Выполнено')
]


class Type(models.Model):
    name = models.CharField(max_length=40, choices=TYPE_CHOICES, default='task', verbose_name='Тип')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'


class Status(models.Model):
    name = models.CharField(max_length=40, choices=STATUS_CHOICES, default='new', verbose_name='Статус')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class Task(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False, verbose_name='Заголовок')
    description = models.TextField(max_length=3000, null=True, blank=True, verbose_name='Описание')
    date = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    type = models.ForeignKey('webapp.Type', related_name='type', on_delete=models.PROTECT, verbose_name='Тип')
    status = models.ForeignKey('webapp.Status', related_name='status', on_delete=models.PROTECT, verbose_name='Статус')

    def __str__(self):
        return "{}. {}".format(self.pk, self.title)

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
