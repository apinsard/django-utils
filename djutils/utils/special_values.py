# -*- coding: utf-8 -*-

__all__ = [
    'NotProvided',
]


class NotProvidedType:

    def __new__(cls):
        try:
            return cls.__instance
        except AttributeError:
            cls.__instance = super().__new__(cls)
            return cls.__instance

    def __bool__(self):
        return False

    def __str__(self):
        return 'NotProvided'

    def __repr__(self):
        return str(self)


NotProvided = NotProvidedType()
