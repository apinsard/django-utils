# -*- coding: utf-8 -*-
from functools import reduce

from django.forms.utils import to_current_timezone
from django.forms.widgets import (
    Widget, MultiWidget, DateInput, TimeInput,
)
from django.utils.formats import get_format

__all__ = [
    'DatePickerWidget', 'TimePickerWidget', 'SplitDateTimePickerWidget',
]


class DatetimePickerMixin(Widget):
    """Base class form date picker and time picker."""

    class Media:
        css = {
            'all': [
                'lib/pickadate/themes/default.css',
                'lib/pickadate/themes/default.date.css',
            ],
        }
        js = [
            'lib/jquery/jquery.js',
            'lib/pickadate/picker.js',
            'lib/pickadate/translations/fr_FR.js',
            # TODO Import translations only when needed.
        ]

    fmt_trans_table = [
        ('%d', 'dd'),
        ('%a', 'ddd'),
        ('%A', 'dddd'),
        ('%m', 'mm'),
        ('%b', 'mmm'),
        ('%B', 'mmmm'),
        ('%y', 'yy'),
        ('%Y', 'yyyy'),
        ('%H', 'HH'),
        ('%M', 'i'),
        ('%p', 'A'),
    ]
    """Translation table from python format to pickadate format."""

    picker_class = None
    """Class to add to the input field to identify the picker."""

    def get_format(self):
        """Return default input format."""
        return get_format(self.format_key)[0]

    def get_client_format(self):
        """Return default input format so that it is understandable by the
        client-end.
        """
        return self.format_to_client_format(self.get_format())

    def format_to_client_format(self, fmt):
        """Translate python datetime format to pickadate format"""
        return reduce(lambda x, y: x.replace(*y), self.fmt_trans_table, fmt)

    def render(self, name, value, attrs=None):
        if attrs is not None:
            attrs = attrs.copy()
        else:
            attrs = {}
        attrs.update(self.attrs)
        if 'class' not in attrs:
            attrs['class'] = self.picker_class
        else:
            attrs['class'] += ' {}'.format(self.picker_class)
        attrs['data-format'] = self.get_client_format()
        return super().render(name, value, attrs)


class DatePickerWidget(DateInput, DatetimePickerMixin):
    """A date input with a javascript picker widget."""

    class Media(DatetimePickerMixin.Media):
        js = DatetimePickerMixin.Media.js + [
            'lib/pickadate/picker.date.js',
        ]

    picker_class = 'datepicker'


class TimePickerWidget(TimeInput, DatetimePickerMixin):
    """A time input with a javascript picker widget."""

    class Media(DatetimePickerMixin.Media):
        js = DatetimePickerMixin.Media.js + [
            'lib/pickadate/picker.time.js',
        ]

    picker_class = 'timepicker'


class SplitDateTimePickerWidget(MultiWidget):
    """A datetime input with separated date and time picker widgets."""

    def __init__(self, attrs=None, date_format=None, time_format=None):
        widgets = (DatePickerWidget(attrs=attrs, format=date_format),
                   TimePickerWidget(attrs=attrs, format=time_format))
        super().__init__(widgets, attrs)

    def format_output(self, rendered_widgets):
        return ('<div class="row">'
                '<div class="col-sm-6">{}</div>'
                '<div class="col-sm-6">{}</div>'
                '</div>').format(*rendered_widgets)

    def decompress(self, value):
        if value:
            value = to_current_timezone(value)
            return [value.date(), value.time().replace(microsecond=0)]
        return [None, None]
