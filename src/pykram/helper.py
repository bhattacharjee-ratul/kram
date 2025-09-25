from .types import OutputField, InputField

def parse_inputfields(executable_instance, context):
    input_parameters = {}
    for field_name, field_definition in executable_instance.__dict__.items():
        if field_definition.__class__ == InputField:
            value_of_field = context.get(field_name)
            # validate the datatype of the field
            if field_definition.validate_datatype:
                if type(value_of_field) != field_definition.datatype:
                    raise Exception(f"Wrong datatype provided for field {field_name}")
            input_parameters[field_name] = value_of_field
    return input_parameters

def parse_output_fields(executable_instance, context):
    print("[DEBUG] PArsing output fields")
    result = {}
    for field_name, field_definition in executable_instance.__dict__.items():
        if field_definition.__class__ == OutputField:
            value_of_field = context.get(field_definition.context_name)
            if field_definition.validate_datatype:
                if type(value_of_field) != field_definition.datatype:
                    raise Exception(f"Wrong datatype provided for output field {field_name}")
            result[field_name] = value_of_field
    return result



