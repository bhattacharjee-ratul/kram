from abc import ABC, abstractmethod
class Field(ABC):
    field_name = None
    default = None
    datatype = None
    validate_datatype=False

class InputField(Field):
    def __init__(self, fieldname, default=None, type=str, context_name=None, validate_datatype=False):
        self.field_name = fieldname
        self.context_name = context_name if context_name else fieldname
        self.default = default
        self.datatype= type
        self.validate_datatype = False
        
class OutputField(Field):

    def __init__(self, fieldname,  type=str, context_name=None, validate_datatype=False):
        self.field_name = fieldname
        self.context_name = context_name if context_name else fieldname
        self.datatype= type
        self.validate_datatype = validate_datatype

class VariableSet:
    def __init__(self, **kwargs):
        pass
    

def declare_field(input_var:Field):
    def wrapper(instance):
        field_name = input_var.field_name
        print(f"Instance: {instance} | field: {field_name}")
        setattr(instance, field_name, input_var)
        return instance
    return wrapper

def define_schema(transformation_function):
    def class_decorator(cls):
        original_new = cls.__new__
        def decorated_new(c, *args, **kwargs):
            if original_new is object.__new__:
                instance = original_new(c)
            else:
                instance = original_new(c, *args, **kwargs)
            if instance is not None:
                instance = transformation_function(instance)
            return instance
        cls.__new__ = staticmethod(decorated_new)
        return cls
    return class_decorator