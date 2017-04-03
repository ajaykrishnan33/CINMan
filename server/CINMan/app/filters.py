import django_filters
from app.models import *

def make_model_filter(model , exclude_fields=(), **kwargs):

    FIELD_REQUIREMENTS = {

        'IntegerField' : ['exact' , 'lt' , 'lte' , 'gt', 'gte'] ,
        'BooleanField' : ['exact'],
        'CharField' : ['exact' ,'iexact', 'contains' , 'startswith'] ,
        'TextField' : ['exact' , 'iexact','contains' , 'startswith'] ,
        'DateTimeField' : [ 'exact'  , 'year' , 'month' , 'week_day' , 'day' , 'lt' , 'gt', 'lte', 'gte' , 'hour' , 'minute'] ,
        'DurationField' : [ 'exact'  , 'day' , 'lt' , 'gt' , 'lte' , 'gte' , 'hour' , 'minute'] ,
        'Relation' : ['exact' , 'isnull'],
    }
    fields = model._meta.get_fields() #returns fields of a model
    fields_of_filter = {}
    for field in fields:
        if not field.name in exclude_fields:
            if field.is_relation:
                requirements = FIELD_REQUIREMENTS['Relation']
                fields_of_filter[field.name] = requirements


            elif field.get_internal_type() in FIELD_REQUIREMENTS.keys():
                requirements = FIELD_REQUIREMENTS[field.get_internal_type()]
                fields_of_filter[field.name] = requirements


            # else:
            #     fields_of_filter[field.name] = ['exact']


    filter_overrides = {
        models.DateTimeField : {
            'filter_class' : django_filters.IsoDateTimeFilter,
        }
    }


    Meta = type('Meta', (), {'model': model , 'fields' : fields_of_filter, 'filter_overrides' : filter_overrides})
    class_fields = {
        'Meta':Meta ,
        '__module__':model.__module__,
    }

    for key , value in kwargs.iteritems():
        filter_name = key + "_filter"
        class_fields[key] = django_filters.CharFilter(method=filter_name)
        class_fields[filter_name] = value


    Filter = type('Filter' , (django_filters.rest_framework.FilterSet,) , class_fields)

    return Filter

MachineFilter = make_model_filter(Machine, ())
CINManUserFilter = make_model_filter(CINManUser, ())
MachineUserFilter = make_model_filter(MachineUser, ())
MachineLoginSessionFilter = make_model_filter(MachineLoginSession, ())
LogEntryFilter = make_model_filter(LogEntry, ())
