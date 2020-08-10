from django.db import models


DEFAULT_TYPE = 'task'
TYPE_CHOICES = [
    (DEFAULT_TYPE, 'Задача'),
    ('bug', 'Ошибка'),
    ('enhancement', 'Улучшение')
]

DEFAULT_STATUS = 'new'
STATUS_CHOICES = [
    (DEFAULT_STATUS, 'Новый'),
    ('in_progress', 'В процессе'),
    ('done', 'Выполнено')
]


class Type(models.Model):
    name = models.CharField(max_length=40, choices=TYPE_CHOICES, default=DEFAULT_TYPE, verbose_name='Тип')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'


class Status(models.Model):
    name = models.CharField(max_length=40, choices=STATUS_CHOICES, default=DEFAULT_STATUS, verbose_name='Статус')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class Task(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False, verbose_name='Заголовок')
    description = models.TextField(max_length=3000, null=True, blank=True, verbose_name='Описание')
    date = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    type = models.ManyToManyField('webapp.Type', related_name='tasks', blank=True)
    status = models.ForeignKey('webapp.Status', related_name='status', on_delete=models.PROTECT, verbose_name='Статус')

    def __str__(self):
        return "{}. {}".format(self.pk, self.title)

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
