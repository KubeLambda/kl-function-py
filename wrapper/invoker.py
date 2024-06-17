import importlib.util

file_path = '/home/lambda/lambda_handler.py'
module_name = 'lambda_handler'

spec = importlib.util.spec_from_file_location(module_name, file_path)

if spec:
    module = importlib.util.module_from_spec(spec)
    if spec.loader:
        spec.loader.exec_module(module)
    else:
        raise Exception("Spec loader didn't initialized")
else:
    raise Exception("No 'lambda_handler.py' was found")

def invoke(event, context):
    module.lambda_handler(event, context)
