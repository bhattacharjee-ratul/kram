from .types import InputField
def run_workflow(workflow_class, **kwargs):
    # Create a Execution object
    print("Within run_workflow")
    wf_instance = workflow_class()
    setattr(wf_instance, "context", {})
    run_executable_with_parameters(wf_instance, kwargs)

def run_executable_with_parameters(executable_instance, context):
    # Form the input parameters for the run function
    input_parameters = {}
    for field_name, field_definition in executable_instance.__dict__.items():
        if field_definition.__class__ == InputField:
            value_of_field = context.get(field_name)
            # validate the datatype of the field
            if field_definition.validate_datatype:
                if type(value_of_field) != field_definition.datatype:
                    raise Exception(f"Wrong datatype provided for field {field_name}")
            input_parameters[field_name] = value_of_field
        

    print(f"For running: {executable_instance.__class__.__name__}; input params: {input_parameters}")
    response = getattr(executable_instance, "run")(**input_parameters)
    return response
    
