from django import template
from gym.models import *

register = template.Library()


@register.simple_tag()
def get_muscle_groups():
    return MuscleGroup.objects.all()


@register.simple_tag()
def get_difficulty_scale():
    return SExercise.DIFFICULTY_SCALE


@register.inclusion_tag('gym/tag_templates/universal_sidebar.html')
def show_difficulty_scale():
    difficulty_set = [UsefulDifficulty(elem) for elem in SExercise.DIFFICULTY_SCALE]
    return {
        'objects_query': difficulty_set
    }


@register.simple_tag()
def get_equipment_types():
    return SEquipmentType.objects.all()


@register.inclusion_tag('gym/tag_templates/universal_sidebar.html')
def show_equipment_types():
    equipment_types = SEquipmentType.objects.all()
    return {
        'objects_query': equipment_types
    }


@register.inclusion_tag('gym/tag_templates/universal_sidebar.html')
def show_muscle_groups():
    m_groups = MuscleGroup.objects.all()
    return {
        'objects_query': m_groups,
    }


# @register.inclusion_tag('gym/tag_templates/list_muscle_groups.html')
# def show_muscle_groups():
#     m_groups = MuscleGroup.objects.all()
#     return {
#         'muscle_groups': m_groups,
#     }


# @register.inclusion_tag('gym/list_muscle_groups.html')
# def show_muscle_groups(arg1='Hello', arg2='world'):
#     m_groups = MuscleGroup.objects.all()
#     return {
#         'muscle_groups': m_groups,
#         'arg1': arg1,
#         'arg2': arg2
#     }
