# -*- coding: utf-8 -*-


def committable(func=None, default=False, only=None):
    """Decorator to make a model method committable.
    This adds support for a 'commit' keyword argument to the method.
    If this argument is set to True, the model instance will be automatically
    saved after this function.

    - `default` sets the default 'commit' value if not provided.
    - `only` defines the subset of fields to save, if not all. It will be
      passed as-is to the `update_fields` argument of the `save()` method.

    Usage
    =====

    @committable
    def some_method(self):
        self.foo = "bar"

    @comittable(default=True, only=['foo', 'bar'])
    def some_method(self, value):
        self.foo = 'bar'
        self.bar = value
    """
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            commit = kwargs.pop('commit', default)
            result = func(self, *args, **kwargs)
            if commit:
                self.save(update_fields=only)
            return result
        wrapper.alters_data = True
        return wrapper

    if func is None:
        return decorator
    elif callable(func):
        return decorator(func)
    else:
        raise ValueError("Invalid arguments provided to committable")
