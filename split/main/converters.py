# converters.py
from django.urls.converters import UUIDConverter

class HyphenlessUUIDConverter(UUIDConverter):
    regex = '[0-9a-f]{32}'

    def to_python(self, value):
        # Добавляем дефисы в UUID
        value = '-'.join([value[:8], value[8:12], value[12:16], value[16:20], value[20:]])
        return super().to_python(value)