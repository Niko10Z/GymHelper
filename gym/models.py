from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator


# Мускул
class Muscle(models.Model):
    # Django создаст поле id сам
    # id = models.fields.IntegerField
    name = models.CharField(verbose_name='Наименование', max_length=50, db_index=True)
    about = models.TextField(verbose_name='Инфо', blank=True)
    # Может быть default(True/False)
    # is_big = models.BooleanField(verbose_name='Крупная?', blank=True)
    muscle_group = models.ForeignKey(
        'MuscleGroup',
        verbose_name='Группа мышц',
        on_delete=models.PROTECT,
        # blank=True,
        # null=True
    )
    created_at = models.DateTimeField(verbose_name='Создано', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Обновлено', auto_now=True)
    # Сохранит в папку images внутри неё создать папку года, месяца, дня
    photo = models.ImageField(verbose_name='Изображение', upload_to='images/muscles', blank=True, null=True)
    # photo = models.ImageField(upload_to='gum/images/%Y/%m/%d', blank=True)

    # Текстовое отображение объекта
    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        # route name, params for making the route(urls.py)
        return reverse('muscle', kwargs={'muscle_id': self.pk})

    # Класс для кастомизации в админке
    class Meta:
        # Имя ед.число
        verbose_name = 'Мускул'
        # Имя мн.числа
        verbose_name_plural = 'Мускулы'
        # Ориентация при отображении в приложении
        ordering = ['name']


# Группа мускулов
class MuscleGroup(models.Model):
    # id = models.fields.IntegerField
    name = models.CharField(verbose_name='Наименование', max_length=50, db_index=True)
    about = models.TextField(verbose_name='Инфо', blank=True)
    # Может быть default(True/False)
    is_big = models.BooleanField(verbose_name='Крупная?', blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='Создано', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Обновлено', auto_now=True)

    # Текстовое отображение объекта
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # route name, params for making the route(urls.py)
        return reverse('muscle_group', kwargs={'pk': self.pk})

    # Класс для кастомизации в админке
    class Meta:
        # Имя ед.число
        verbose_name = 'Группа мускулов'
        # Имя мн.число
        verbose_name_plural = 'Группы мускулов'
        # Ориентация при отображении в приложении
        ordering = ['-is_big', 'name']

    def get_tree_first(self):
        return Muscle.objects.filter(muscle_group_id=self.pk).order_by("name")[:3]

    def get_all_muscles(self):
        return Muscle.objects.filter(muscle_group_id=self.pk).order_by("name")


# Тип спорт.инвентаря
class SEquipmentType(models.Model):
    name = models.CharField(verbose_name='Наименование', max_length=50, db_index=True)
    about = models.TextField(verbose_name='Инфо', blank=True)

    created_at = models.DateTimeField(verbose_name='Создано', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Обновлено', auto_now=True)

    # Текстовое отображение объекта
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # route name, params for making the route(urls.py)
        return reverse('equipments', kwargs={'id_type': self.pk})

    # Класс для кастомизации в админке
    class Meta:
        # Имя ед.число
        verbose_name = 'Тип инвентаря'
        # Имя мн.число
        verbose_name_plural = 'Типы инвентаря'
        # Ориентация при отображении в приложении
        ordering = ['name']


class SEquipment(models.Model):
    name = models.CharField(
        verbose_name='Наименование',
        max_length=50
    )
    about = models.TextField(
        verbose_name='Инфо',
        blank=True
    )
    eq_type = models.ForeignKey(
        'SEquipmentType',
        verbose_name='Тип инвентаря',
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(verbose_name='Создано', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Обновлено', auto_now=True)
    # Сохранит в папку images внутри неё создать папку года, месяца, дня
    photo = models.ImageField(verbose_name='Изображение', upload_to='images/equipments', blank=True, null=True)

    # Текстовое отображение объекта
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # route name, params for making the route(urls.py)
        return reverse('equipment', kwargs={'pk': self.pk})

    # Класс для кастомизации в админке
    class Meta:
        # Имя ед.число
        verbose_name = 'Спорт.инвентарь'
        # Имя мн.числа
        verbose_name_plural = 'Спорт.инвентарь'
        # Ориентация при отображении в приложении
        ordering = ['name',]


class UsefulDifficulty():
    def __init__(self, difficulty_tuple):
        self.name = f'Сложность - {difficulty_tuple[1]}'
        self.val = difficulty_tuple[0]

    def get_absolute_url(self):
        if self.val is not None:
            # route name, params for making the route(urls.py)
            return reverse('exercise_by_diff', kwargs={'difficulty': self.val})
        else:
            return reverse('exercises')


# Спорт.упражнение
class SExercise(models.Model):
    # Шкала сложности 0-наилегчайшее
    DIFFICULTY_SCALE = [
        (0, '00'),
        (1, '01'),
        (2, '02'),
        (3, '03'),
        (4, '04'),
        (5, '05'),
        (6, '06'),
        (7, '07'),
        (8, '08'),
        (9, '09'),
        (10, '10'),
    ]
    difficulty = models.PositiveSmallIntegerField(
        verbose_name='Сложность',
        choices=DIFFICULTY_SCALE,
        default=0,
    )
    name = models.CharField(
        verbose_name='Наименование',
        max_length=50
    )
    about = models.TextField(verbose_name='Методика выполнения', blank=True)
    created_at = models.DateTimeField(verbose_name='Создано', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Обновлено', auto_now=True)

    # equipment = models.ForeignKey(
    #     'SEquipment',
    #     verbose_name='Требуемое оборудование',
    #     on_delete=models.PROTECT,
    #     blank=True,
    #     null=True
    # )
    # muscle_using = models.OneToOneField(
    #     MuscleUsing,
    #     on_delete=models.CASCADE,
    #     blank=True,
    #     null=True
    # )
    # muscle = models.ForeignKey(
    #     'Muscle',
    #     verbose_name='Целевой мускул',
    #     on_delete=models.PROTECT
    # )

    # Текстовое отображение объекта
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # route name, params for making the route(urls.py)
        return reverse('exercise', kwargs={'pk': self.pk})

    # Класс для кастомизации в админке
    class Meta:
        # Имя ед.число
        verbose_name = 'Упражнение'
        # Имя мн.числа
        verbose_name_plural = 'Упражнения'
        # Ориентация при отображении в приложении
        ordering = ['name', ]


# Включение мускула в упражнение
class MuscleUsing(models.Model):
    # Прорабатываемый мускул
    muscle = models.ForeignKey(
        'Muscle',
        verbose_name='Прорабатываемый мускул',
        on_delete=models.CASCADE
    )
    # Процент включения
    using_perc = models.PositiveSmallIntegerField(
        verbose_name='Процент включения',
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ],
    )
    s_exercise = models.ForeignKey(
        'SExercise',
        verbose_name='Упражнение',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(verbose_name='Создано', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Обновлено', auto_now=True)

    # Текстовое отображение объекта
    def __str__(self):
        return f'{self.muscle.name}({self.using_perc}%)'

    # Класс для кастомизации в админке
    class Meta:
        # Имя ед.число
        verbose_name = 'Использование мускула'
        # Имя мн.числа
        verbose_name_plural = 'Использование мускулов'
        # Ориентация при отображении в приложении
        ordering = ['id', ]


# Использование инвентаря в упражнении
class EquipmentUsing(models.Model):
    # Используемый инвентарь
    equipment = models.ForeignKey(
        'SEquipment',
        verbose_name='Используемый инвентарь',
        on_delete=models.CASCADE
    )
    s_exercise = models.ForeignKey(
        'SExercise',
        verbose_name='Упражнение',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(verbose_name='Создано', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Обновлено', auto_now=True)

    # Текстовое отображение объекта
    def __str__(self):
        return f'{self.equipment.name}'

    # Класс для кастомизации в админке
    class Meta:
        # Имя ед.число
        verbose_name = 'Использование инвентаря'
        # Имя мн.числа
        verbose_name_plural = 'Использование инвентаря'
        # Ориентация при отображении в приложении
        ordering = ['id', ]


# Спортивная тренировка
class STraining(models.Model):
    name = models.CharField(
        verbose_name='Наименование',
        max_length=50,
        default='Тренировка'
    )
    training_date = models.DateField(
        verbose_name='Дата тренировки'
    )

    about = models.TextField(verbose_name='Пояснение', blank=True)

    def __str__(self):
        if self.about:
            return f'{self.name} от {self.training_date}({self.about})'
        else:
            return f'{self.name} от {self.training_date}'

    # Класс для кастомизации в админке
    class Meta:
        # Имя ед.число
        verbose_name = 'Спорт.тренировка'
        # Имя мн.числа
        verbose_name_plural = 'Спорт.тренировки'
        # Ориентация при отображении в приложении
        ordering = ['training_date',]

    def get_absolute_url(self):
        # route name, params for making the route(urls.py)
        return reverse('straining', kwargs={'pk': self.pk})


# Одно упражнение в тренировке
class TrainingExercise(models.Model):
    s_training = models.ForeignKey(
        'STraining',
        verbose_name='Тренировка',
        on_delete=models.CASCADE
    )
    s_exercise = models.ForeignKey(
        'SExercise',
        verbose_name='Упражнение',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.s_exercise.name}'

    # Класс для кастомизации в админке
    class Meta:
        # Имя ед.число
        verbose_name = 'Упражнение тренировки'
        # Имя мн.числа
        verbose_name_plural = 'Упражнения тренировки'
        # Ориентация при отображении в приложении
        ordering = ['s_training',]


# Один раунд упражнения тренировки
class TrainingRound(models.Model):
    weight = models.FloatField(verbose_name='Вес', blank=True, null=True)
    plan_try = models.IntegerField(verbose_name='Повторов(план)')
    fact_try = models.IntegerField(verbose_name='Повторов(факт)', blank=True, null=True)
    training_exercise = models.ForeignKey(
        'TrainingExercise',
        verbose_name='Упражнение тренировки',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.training_exercise.s_exercise.name}(вес: {self.weight or "0.00"}, повторов: {self.plan_try} / {self.fact_try or "0"})'

    # Класс для кастомизации в админке
    class Meta:
        # Имя ед.число
        verbose_name = 'Раунд тренировки'
        # Имя мн.числа
        verbose_name_plural = 'Раунды тренировки'
        # Ориентация при отображении в приложении
        ordering = ['pk',]
