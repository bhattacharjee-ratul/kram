def parse_inputfields(params):
    for key, value in params.items():
        print(f"{key} -> Type of {value.__class__.__name__}")
