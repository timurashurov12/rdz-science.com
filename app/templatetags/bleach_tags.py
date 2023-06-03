from django import template
import bleach

register = template.Library()

@register.filter
def bleach_clean(value, max_length=100):
    cleaned_value = bleach.clean(value, tags=[], strip=True)
    cleaned_value = cleaned_value.replace('&nbsp;', '')  # Удалить символы отступа
    cleaned_value = cleaned_value.strip()  # Удалить начальные и конечные пробелы
    cleaned_value = cleaned_value.replace('\n\n', '')  # Заменить пустые строки на закрывающий и открывающий теги параграфа
    cleaned_value = cleaned_value.replace('\n', '<br>')  # Заменить символы новой строки на тег переноса строки
    cleaned_value = cleaned_value.replace('<hr>', '')  # Удалить тег <hr> полностью

    if len(cleaned_value) > max_length:
        cleaned_value = cleaned_value[:max_length] + '...'  # Ограничить текст до максимальной длины и добавить многоточие

    cleaned_value = '<div style="text-align: left; word-wrap: break-word;">{}</div>'.format(cleaned_value)  # Применить выравнивание текста по левому краю и обернуть в div с переносом слов

    return cleaned_value