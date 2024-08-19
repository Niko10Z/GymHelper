from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


# Кастомизация отображения в админке
# class Admin(admin.ModelAdmin):
#     # Что показывать
#     list_display = ()
#     # Что служит ссылкой на открытие объекта
#     list_display_links = ()
#     # По чему поиск
#     search_fields = ()
#     # Поля, редактируемые прямо в дереве
#     list_editable = ()
#     # Поля, по которым можно фильтровать
#     list_filter = ()


# Кастомизация отображения в админке
class MuscleAdmin(admin.ModelAdmin):
    # Что показывать
    list_display = (
        'id',
        'name',
        'muscle_group',
        'created_at',
        'updated_at')
        # 'updated_at',
        # 'get_photo')
    # Что служит ссылкой на открытие объекта
    list_display_links = ('id', 'name')
    # По чему поиск
    search_fields = ('name',)
    # Поля, редактируемые прямо в дереве
    list_editable = ('muscle_group',)
    # Поля, по которым можно фильтровать
    list_filter = ('muscle_group',)
    # Список отобр-х полей внутри объекта
    fields = (
        'name',
        'muscle_group',
        'get_photo',
        'created_at',
        'updated_at'
    )
    # Нередактируемые поля
    readonly_fields = (
        'get_photo',
        'created_at',
        'updated_at'
    )
    # Чтобы панель редактирования была не только снизу,
    # но и вверху
    save_on_top = True

    # Для вывода в админке не ссылки на фото, а самого изобр-я
    # название - любое(не зарезервировано)
    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="75px">')
        # else:
        #     return 'Фото отсутствует'

    # Указывает как подписать вывод функции
    get_photo.short_description = 'Изображение'


# Кастомизация отображения в админке
class MuscleGroupAdmin(admin.ModelAdmin):
    # Что показывать
    list_display = ('id', 'name', 'created_at', 'updated_at')
    # Что служит ссылкой на открытие объекта
    list_display_links = ('id', 'name')
    # По чему поиск
    search_fields = ('name',)


# Кастомизация отображения в админке
class SEquipmentAdmin(admin.ModelAdmin):
    # Что показывать
    list_display = ('id', 'name', 'eq_type')
    # Что служит ссылкой на открытие объекта
    list_display_links = ('id', 'name')
    # По чему поиск
    search_fields = ('name', 'eq_type')
    # Поля, редактируемые прямо в дереве
    # list_editable = ('name',)
    # Поля, по которым можно фильтровать
    list_filter = ('name', 'eq_type')


# Кастомизация отображения в админке
class SExerciseAdmin(admin.ModelAdmin):
    # Что показывать
    list_display = ('id', 'name', 'difficulty')
    # Что служит ссылкой на открытие объекта
    list_display_links = ('id', 'name')
    # По чему поиск
    search_fields = ('name', 'difficulty')
    # Поля, редактируемые прямо в дереве
    list_editable = ('difficulty',)
    # Поля, по которым можно фильтровать
    list_filter = ('name', 'difficulty')


admin.site.register(Muscle, MuscleAdmin)
admin.site.register(MuscleGroup, MuscleGroupAdmin)
admin.site.register(SEquipment, SEquipmentAdmin)
admin.site.register(SExercise, SExerciseAdmin)
admin.site.register(MuscleUsing)
admin.site.register(EquipmentUsing)
admin.site.register(STraining)
admin.site.register(TrainingExercise)
admin.site.register(TrainingRound)
admin.site.register(SEquipmentType)

# Кастомизация тайтла и хедера в меню админки
admin.site.site_title = 'Управление программой тренировок'
admin.site.site_header = 'Управление программой тренировок'