# -*- coding: utf-8 -*-
import csv
from datetime import date, datetime, time

from django.http import HttpResponse
from django.utils import timezone
from django.utils.translation import ugettext_lazy


def _get_field_value(obj, field_name):
    value = getattr(obj, field_name)
    if value is None:
        return 'NULL'
    if isinstance(value, bool):
        return '1' if value else '0'
    if isinstance(value, (date, datetime, time)):
        return value.isoformat()
    return str(value)


def export_as_csv(modeladmin, request, queryset):
    """Export selected objects as CSV (simple version)
    Export all concrete fields of the model.

    - Foreign keys are not dereferenced, only the primary key is exported
    - `None` values are exported as string "NULL"
    - Boolean values are exported as "0" for False and "1" for True
    - Dates, times and datetimes are exported as ISO format
    - All other types are exported as strings using their `__str__()` method

    The CSV file is named after the following format:
        "{app}_{model}-%Y%m%d_%H%M.csv"

    For customization of the output, use `advanced_export`.
    """
    opts = modeladmin.model._meta
    filename = format(timezone.now(), '{app}_{model}-%Y%m%d_%H%M.csv').format(
        app=opts.app_label, model=opts.model_name)

    response = HttpResponse(content_type='text/csv')
    content_disposition = 'attachment; filename="{}"'.format(filename)
    response['Content-Disposition'] = content_disposition

    writer = csv.writer(response)
    field_names = [f.get_attname() for f in opts.concrete_fields]
    writer.writerow(field_names)
    for obj in queryset.only(field_names):
        writer.writerow([_get_field_value(obj, f) for f in field_names])

    return response

export_as_csv.short_description = ugettext_lazy("Export as CSV")


def advanced_export(modeladmin, request, queryset):
    """Export selected objects according to customizable settings

    - Supported output fomats are: CSV, JSON, XML and YAML
    - Exported fields can be selected
    - Output format of the fields can be selected
    - Compression of the output file can be selected

    Output file name can be selected. Default is:
        "{app}_{model}-%Y%m%d_%H%M.{format_extension}"
    """
    raise NotImplementedError

advanced_export.short_description = ugettext_lazy("Advanced export")
