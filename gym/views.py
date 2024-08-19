from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Muscle, MuscleGroup, SEquipment, SExercise, STraining, TrainingExercise, MuscleUsing, \
    EquipmentUsing, TrainingRound, SEquipmentType
from django.template.defaulttags import register
from .forms import MuscleForm, SExerciseForm, SEquipmentForm, TrainingRoundForm, TrainingExerciseForm, STrainingForm, \
    EquipmentUsingForm, MuscleUsingForm, STrainingFullForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


@register.filter
def get_item(collection, key):
    if isinstance(collection, dict):
        return collection.get(key, None)
    else:
        return collection[key]


class HomeGym(ListView):
    model = Muscle
    # Можно самому задать имя шаблона для отображения
    # по умолчанию *имя класса в нижнем регистре*_list.html
    # template_name = ''
    # Можно самому задать имя объекта с данными(по умолчанию object_list)
    # context_object_name = ''
    # Словарь с дополнительными данными
    # рекомендуется использовать для статичных данных
    # (не list, dict и всё, что можно изменить)
    # extra_context = {'val': 'Hello world!',}

    # Для дополнения передаваемых данных ещё чем-то
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['val'] = 'Hello world!'
        return context

    # Для фильтрации данных для вывода
    def get_queryset(self):
        return Muscle.objects.filter(muscle_group=1)


class MusclesByGroup(ListView):
    model = Muscle
    template_name = 'gym/index.html'
    context_object_name = 'muscles'
    allow_empty = False

    def get_queryset(self):
        return Muscle.objects.filter(muscle_group_id=self.kwargs['group_id'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = MuscleGroup.objects.get(pk=self.kwargs['group_id']).name
        return context


class CreateMuscle(CreateView):
    form_class = MuscleForm
    template_name = 'gym/add_muscle.html'
    # Для указания адреса редиректа при успехе
    # по умолчанию get_absolute_url создаваемого класса
    # success_url = reverse_lazy('home')
    extra_context = {'title': 'Добавление мускула', }


class MuscleGroupView(ListView):
    model = MuscleGroup
    template_name = 'gym/muscles.html'
    context_object_name = 'muscle_groups'
    allow_empty = False
    extra_context = {'title': 'Мускулы тела',}
    # queryset = MuscleGroup.objects.select_related('')


class MuscleGroupDetail(DetailView):
    model = MuscleGroup
    # Можно самому задать имя шаблона для отображения
    # по умолчанию *имя класса в нижнем регистре*_detail.html
    # template_name = 'gym/musclegroup_detail.html'
    # Если хотим задать имя параметра для поиска
    # по умолчанию pk или slug
    # pk_url_kwarg = 'group_id'
    # Можно самому задать имя объекта с данными(по умолчанию object)
    # context_object_name = ''

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.model.objects.get(pk=self.kwargs['pk']).name
        return context


class CreateSExercise(CreateView):
    form_class = SExerciseForm
    template_name = 'gym/add_sexercise.html'
    # Для указания адреса редиректа при успехе
    # по умолчанию get_absolute_url создаваемого класса
    # success_url = reverse_lazy('home')
    extra_context = {'title': 'Добавление упражнения', }

    def get_success_url(self):
        print(dir(self.request))
        print(self.request.POST)
        if self.request.POST['return_to']:
            return self.request.POST['return_to']
        else:
            return self.object.get_absolute_url()


class SExerciseView(ListView):
    model = SExercise
    # Можно самому задать имя шаблона для отображения
    # по умолчанию *имя класса в нижнем регистре*_list.html
    template_name = 'gym/sexercise_list.html'
    # Можно самому задать имя объекта с данными(по умолчанию object_list)
    # context_object_name = ''
    # Словарь с дополнительными данными
    # рекомендуется использовать для статичных данных
    # (не list, dict и всё, что можно изменить)
    extra_context = {'title': 'Спортивные упражнения'}
    # Допускать ли пустые queryset
    # allow_empty = False
    allow_empty = True

    def get_queryset(self):
        if 'difficulty' in self.kwargs:
            self.extra_context['difficulty'] = self.kwargs['difficulty']
            return SExercise.objects.filter(difficulty=self.kwargs['difficulty']).order_by("name")[:9]
        self.extra_context['difficulty'] = 'Любая'
        return SExercise.objects.all().order_by("name")[:9]


class SExerciseDetail(DetailView):
    model = SExercise
    template_name = 'gym/exercise.html'
    # pk_url_kwarg = 'exercise_id'
    context_object_name = 'exercise'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.model.objects.get(pk=self.kwargs['pk']).name
        return context


class CreateSEquipment(CreateView):
    form_class = SEquipmentForm
    template_name = 'gym/add_sequipment.html'
    # Для указания адреса редиректа при успехе
    # по умолчанию get_absolute_url создаваемого класса
    # success_url = reverse_lazy('home')
    extra_context = {'title': 'Добавление инвентаря', }


class SEquipmentView(ListView):
    model = SEquipment
    # Можно самому задать имя шаблона для отображения
    # по умолчанию *имя класса в нижнем регистре*_list.html
    template_name = 'gym/sequipment_list.html'
    # Можно самому задать имя объекта с данными(по умолчанию object_list)
    # context_object_name = ''
    # Словарь с дополнительными данными
    # рекомендуется использовать для статичных данных
    # (не list, dict и всё, что можно изменить)
    extra_context = {'title': 'Спортивный инвентарь'}
    allow_empty = True

    def get_queryset(self):
        if 'id_type' in self.kwargs:
            self.extra_context['type'] = SEquipmentType.objects.get(pk=self.kwargs['id_type'])
            return SEquipment.objects.filter(eq_type=self.kwargs['id_type']).order_by("name")[:9]
        self.extra_context['type'] = 'Все типы'
        return SExercise.objects.all().order_by("name")[:9]


class SEquipmentDetail(DetailView):
    model = SEquipment
    # Можно самому задать имя шаблона для отображения
    # по умолчанию *имя класса в нижнем регистре*_detail.html
    # template_name = 'gym/sequipment_detail.html'
    # Если хотим задать имя параметра для поиска
    # по умолчанию pk или slug
    # pk_url_kwarg = 'equipment_id'
    # Можно самому задать имя объекта с данными(по умолчанию object)
    # context_object_name = ''

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.model.objects.get(pk=self.kwargs['pk']).name
        return context


class STrainingDetail(DetailView):
    model = STraining
    # Можно самому задать имя шаблона для отображения
    # по умолчанию *имя класса в нижнем регистре*_detail.html
    # template_name = 'gym/straining_detail.html'
    # Если хотим задать имя параметра для поиска
    # по умолчанию pk или slug
    # pk_url_kwarg = 'equipment_id'
    # Можно самому задать имя объекта с данными(по умолчанию object)
    # context_object_name = ''

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.model.objects.get(pk=self.kwargs['pk'])
        return context


class STrainingView(ListView):
    model = STraining
    template_name = 'gym/straining_list.html'
    extra_context = {'title': 'Спортивные тренировки'}


class CreateSTraining(CreateView):
    form_class = STrainingForm
    template_name = 'gym/add_straining.html'
    extra_context = {'title': 'Добавление тренировки', }

    # def get_success_url(self):
    #     return reverse_lazy('straining', args=(self.object.s_training.pk,))


class UpdateSTraining(UpdateView):
    model = STraining
    form_class = STrainingFullForm
    template_name = 'gym/add_strainingfull.html'
    extra_context = {'title': 'Редактирование тренировки', }


class CreateTrainingExercise(CreateView):
    form_class = TrainingExerciseForm
    template_name = 'gym/add_trainingexercise.html'
    extra_context = {'title': 'Добавление упражнения в тренировку', }

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(dir(context['form']))
        # print(dir(context['form'].fields['s_training']))
        # print(dir(context['view']))
        # print(context['view'].fields)
        # print(self.kwargs)
        if 'straining_id' in self.kwargs:
            context['form'].fields['s_training'].initial = STraining.objects.get(pk=self.kwargs['straining_id'])
        return context

    def get_success_url(self):
        print(dir(self))
        print(self.__dict__)
        return reverse_lazy('straining', args=(self.object.s_training.pk,))


class CreateTrainingRound(CreateView):
    form_class = TrainingRoundForm
    template_name = 'gym/add_traininground.html'
    extra_context = {'title': 'Добавление раунда упражнения', }

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(dir(context['form']))
        # print(dir(context['form'].fields['s_training']))
        # print(dir(context['view']))
        # print(context['view'].fields)
        # print(self.kwargs)
        if 'texercise_id' in self.kwargs:
            context['form'].fields['training_exercise'].initial = TrainingExercise.objects.get(pk=self.kwargs['texercise_id'])
        return context

    def get_success_url(self):
        return reverse_lazy('straining', args=(self.object.training_exercise.s_training.pk,))


class UpdateTrainingRound(UpdateView):
    model = TrainingRound
    form_class = TrainingRoundForm
    template_name = 'gym/add_traininground.html'
    extra_context = {'title': 'Редактирование раунда упражнения', }

    def get_success_url(self):
        return reverse_lazy('straining', args=(self.object.training_exercise.s_training.pk,))


class CreateEquipmentUsing(CreateView):
    form_class = EquipmentUsingForm
    template_name = 'gym/add_equipmentusing.html'
    extra_context = {'title': 'Добавление инвентаря', }

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if 's_exercise_id' in self.kwargs:
            context['form'].fields['s_exercise'].initial = SExercise.objects.get(pk=self.kwargs['s_exercise_id'])
        return context

    def get_success_url(self):
        return reverse_lazy('exercise', args=(self.object.s_exercise.pk,))


class UpdateEquipmentUsing(UpdateView):
    model = EquipmentUsing
    form_class = EquipmentUsingForm
    template_name = 'gym/add_equipmentusing.html'
    extra_context = {'title': 'Редактирование используемого инвентаря', }

    def get_success_url(self):
        return reverse_lazy('exercise', args=(self.object.s_exercise.pk,))


class CreateMuscleUsing(CreateView):
    form_class = MuscleUsingForm
    template_name = 'gym/add_muscleusing.html'
    extra_context = {'title': 'Добавление включения мускула', }

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if 's_exercise_id' in self.kwargs:
            context['form'].fields['s_exercise'].initial = SExercise.objects.get(pk=self.kwargs['s_exercise_id'])
        return context

    def get_success_url(self):
        return reverse_lazy('exercise', args=(self.object.s_exercise.pk,))


class UpdateMuscleUsing(UpdateView):
    model = MuscleUsing
    form_class = MuscleUsingForm
    template_name = 'gym/add_muscleusing.html'
    extra_context = {'title': 'Редактирование включения мускула', }

    def get_success_url(self):
        return reverse_lazy('exercise', args=(self.object.s_exercise.pk,))


# class CreateSTraining(CreateView):
#     form_class = STrainingForm
#     template_name = 'gym/add_straining.html'
#     # Для указания адреса редиректа при успехе
#     # по умолчанию get_absolute_url создаваемого класса
#     # success_url = reverse_lazy('home')
#     extra_context = {'title': 'Создание тренировки', }


def gym_index(request):
    muscles = Muscle.objects.all()
    # m_groups = MuscleGroup.objects.all()
    return render(request,
                  template_name='gym/index.html',
                  context={
                      'title': 'Главная',
                      'welcome': 'Помощник самостоятельных тренировок',
                      'muscles': muscles,
                  })

    # return render(request,
    #               template_name='gym/index.html',
    #               context={
    #                   'title': 'Главная',
    #                   'welcome': 'Помощник самостоятельных тренировок',
    #                   'links': [
    #                       {'link': '/gym', 'text': 'Главная'},
    #                       {'link': '/training', 'text': 'Тренировки'},
    #                       {'link': '/almanac', 'text': 'Альманах'},
    #                       {'link': '/client', 'text': 'Личный кабинет'}
    #                   ],
    #               })


def gym_exercises(request):
    exercises = SExercise.objects.all()
    # имена параметров указывать не обязательно
    # context удобнее вынести в отдельную переменную-dict
    return render(request,
                  template_name='gym/exercises.html',
                  context={
                      'title': 'Спортивные упражнения',
                      'exercises': exercises
                  })


def gym_exercise_by_diff(request, difficulty):
    exercises = SExercise.objects.filter(difficulty=difficulty).order_by('-name')
    # имена параметров указывать не обязательно
    # context удобнее вынести в отдельную переменную-dict
    return render(request,
                  template_name='gym/exercises.html',
                  context={
                      'title': 'Спортивные упражнения',
                      'exercises': exercises
                  })


def gym_exercise(request, exercise_id):
    exercise = get_object_or_404(SExercise, pk=exercise_id)
    # имена параметров указывать не обязательно
    # context удобнее вынести в отдельную переменную-dict
    return render(request,
                  template_name='gym/exercise.html',
                  context={
                      'title': 'Спортивное упражнение',
                      'exercise': exercise
                  })


def gym_equipments(request):
    return HttpResponse('<h1>Инвентарь</h1>')


def gym_muscles(request):
    m_groups = MuscleGroup.objects.all()
    # имена параметров указывать не обязательно
    # context удобнее вынести в отдельную переменную-dict
    return render(request,
                  template_name='gym/muscles.html',
                  context={
                      'title': 'Мускулы тела',
                      'muscle_groups': m_groups
                  })


def gym_client(request):
    # print(request)
    return HttpResponse('<h1>Личный кабинет пользователя.</h1>'
                        '<ul><li>Программы</li>'
                        '<li>тренировки</li>'
                        '<li>рейтинг упражнений</li></ul>'
                        '<ul><li>Возможность создать программу</li>'
                        '<li>Возможность создать тренировку</li></ul>')


def gym_almanac(request):
    # Вместо all() можно использовать order_by(), exclude(), filter(), etc.
    muscles = Muscle.objects.all()
    m_groups = MuscleGroup.objects.all()
    # имена параметров указывать не обязательно
    # context удобнее вынести в отдельную переменную-dict
    # return render(request,
    #               template_name='gym/almanac.html',
    #               context={
    #                   'title': 'Альманах',
    #                   'welcome': 'Добро пожаловать в альманах',
    #                   'header_links': [
    #                       {'link': '/gym', 'text': 'Главная'},
    #                       {'link': '/training', 'text': 'Тренировки'},
    #                       {'link': '/almanac', 'text': 'Альманах'},
    #                       {'link': '/client', 'text': 'Личный кабинет'}
    #                   ],
    #                   'almanac_links': [
    #                       {'link': '/muscles', 'text': 'Мускулы'},
    #                       {'link': '/muscle-groups', 'text': 'Группы мышц'},
    #                       {'link': '/equipments', 'text': 'Оборудование'},
    #                       {'link': '/exercises', 'text': 'Упражнения'}
    #                   ],
    #               })
    return render(request,
                  # template_name='gym/showall.html',
                  template_name='gym/bootstrappage.html',
                  context={
                      'title': 'Альманах',
                      'objs': muscles,
                      'm_groups': m_groups
                  })


def get_muscle_group(request, group_id):
    muscles = Muscle.objects.filter(muscle_group_id=group_id)
    m_groups = MuscleGroup.objects.all()
    m_group = MuscleGroup.objects.get(pk=group_id)
    # имена параметров указывать не обязательно
    # context удобнее вынести в отдельную переменную-dict
    return render(request,
                  # template_name='gym/showall.html',
                  # template_name='gym/bootstrappage.html',
                  template_name='gym/index.html',
                  context={
                      'title': m_group.name,
                      'muscles': muscles,
                      'muscle_groups': m_groups
                  })


def get_muscle(request, muscle_id):
    # muscle = Muscle.objects.get(pk=muscle_id)
    muscle = get_object_or_404(Muscle, pk=muscle_id)
    # имена параметров указывать не обязательно
    # context удобнее вынести в отдельную переменную-dict
    return render(request,
                  template_name='gym/muscle.html',
                  context={
                      'title': muscle.name,
                      'muscle': muscle,
                  })


# Переписано на CreateView -CreateMuscle-
# def add_muscle(request):
#     if request.method == 'POST':
#         form = MuscleForm(data=request.POST, files=request.FILES)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             # print(request.POST)
#             # print(request.FILES)
#             # Если форма НЕ связана с моделью
#             # muscle_obj = Muscle.objects.create(**form.cleaned_data)
#             # Если форма связана с моделью
#             muscle_obj = form.save()
#             return redirect(muscle_obj)
#     else:
#         form = MuscleForm()
#     # имена параметров указывать не обязательно
#     # context удобнее вынести в отдельную переменную-dict
#     return render(request,
#                   template_name='gym/add_muscle.html',
#                   context={
#                       'title': 'Добавление мускула',
#                       'form': form
#                   })
