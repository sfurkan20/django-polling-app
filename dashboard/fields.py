from django.db import models

class PollOption():
    def __init__(self, name, voteCount=0):
        self.name = name
        self.voteCount = voteCount

class PollOptionField(models.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not kwargs.get("max_length"):
            self.max_length = 150

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        return name, path, args, kwargs

    def get_prep_value(self, value):
        return f"{value.name}~{value.voteCount}"

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return self.to_python(value)

    def to_python(self, value:str):
        if not value or isinstance(value, PollOption):
            return value

        separatorIndex = value.index('~')
        return PollOption(value[:separatorIndex], int(value[separatorIndex + 1:]))