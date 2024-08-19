from django import forms
from .models import *
import re
from django.core.exceptions import ValidationError


class MuscleFormWithoutModel(forms.Form):
    name = forms.CharField(
        max_length=50,
        label='Наименование',
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    about = forms.CharField(
        label='Описание',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': '5'
        })
    )
    muscle_group = forms.ModelChoiceField(
        queryset=MuscleGroup.objects.all(),
        label='Группа мышц',
        empty_label='Выберите группу',
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )


# class STrainingFullForm(forms.Form):
#     training_date = forms.DateField(
#         label='Дата тренировки',
#         required=True,
#         widget=forms.SelectDateWidget(attrs={
#             'class': 'form-control',
#             'type': 'date',
#             'placeholder': '__.__.____',
#         })
#     )
#     trainingexercise_set = forms.ModelChoiceField(
#         queryset=TrainingExercise.objects.all(),
#         label='Упражнения',
#         empty_label='Выберите упражнение',
#         required=False,
#         widget=forms.Select(attrs={
#             'class': 'form-control',
#         })
#     )


class STrainingFullForm(forms.ModelForm):
    class Meta:
        model = STraining
        fields = ['training_date', 'about']
        widgets = {
            'training_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'placeholder': '__.__.____',
            }),
            'about': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '5',
            }),
        }

    trainingexercise_set = forms.ModelChoiceField(
        queryset=TrainingExercise.objects.filter(s_training=4),
        label='Упражнения',
        empty_label=None,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )


class MuscleForm(forms.ModelForm):
    class Meta:
        model = Muscle
        # fields = '__all__'
        fields = ['name', 'about', 'muscle_group', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'about': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '5'
            }),
            'muscle_group': forms.Select(attrs={
                'class': 'form-control',
            }),
            'photo': forms.FileInput(),
        }

    # Кастомный валидатор. Отрабатывает после встроенного
    # clean_*имя поля для валидирования*
    def clean_name(self):
        # self - вся форма
        name = self.cleaned_data['name']
        if re.search(r'\d', name):
            raise ValidationError('Название не должно содержать цифр')
        return name


class SEquipmentForm(forms.ModelForm):
    class Meta:
        model = SEquipment
        fields = ['name', 'about', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'about': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '5'
            }),
            'photo': forms.FileInput(),
        }


class SExerciseForm(forms.ModelForm):
    class Meta:
        model = SExercise
        fields = ['name', 'about', 'difficulty']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'about': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '5'
            }),
            'difficulty': forms.Select(attrs={
                'class': 'form-control',
            }),
        }


class STrainingForm(forms.ModelForm):
    class Meta:
        model = STraining
        fields = ['training_date', 'about']
        widgets = {
            'training_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'placeholder': '__.__.____',
            }),
            'about': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '5',
            }),
        }


class TrainingExerciseForm(forms.ModelForm):
    class Meta:
        model = TrainingExercise
        fields = ['s_training', 's_exercise']
        widgets = {
            # 's_training': forms.Select(attrs={
            #     'class': 'form-control',
            # }),
            's_training': forms.HiddenInput(),
            's_exercise': forms.Select(attrs={
                'class': 'form-control',
            }),
        }

    # s_training = forms.ModelChoiceField(queryset=STraining.objects.filter(pk=),initial=0)


class TrainingRoundForm(forms.ModelForm):
    class Meta:
        model = TrainingRound
        fields = ['training_exercise', 'plan_try', 'weight', 'fact_try']
        widgets = {
            # 'training_exercise': forms.Select(attrs={
            #     'class': 'form-control',
            # }),
            'training_exercise': forms.HiddenInput(),
            'plan_try': forms.NumberInput(attrs={
                'class': 'form-control',
            }),
            'weight': forms.NumberInput(attrs={
                'class': 'form-control',
            }),
            'fact_try': forms.NumberInput(attrs={
                'class': 'form-control',
            }),
        }


class MuscleUsingForm(forms.ModelForm):
    class Meta:
        model = MuscleUsing
        fields = ['muscle', 'using_perc', 's_exercise']
        widgets = {
            # 'training_exercise': forms.Select(attrs={
            #     'class': 'form-control',
            # }),
            's_exercise': forms.HiddenInput(),
            'muscle': forms.Select(attrs={
                'class': 'form-control',
            }),
            'using_perc': forms.NumberInput(attrs={
                'class': 'form-control',
            }),
        }


class EquipmentUsingForm(forms.ModelForm):
    class Meta:
        model = EquipmentUsing
        fields = ['equipment', 's_exercise']
        widgets = {
            # 'training_exercise': forms.Select(attrs={
            #     'class': 'form-control',
            # }),
            's_exercise': forms.HiddenInput(),
            'equipment': forms.Select(attrs={
                'class': 'form-control',
            }),
        }
