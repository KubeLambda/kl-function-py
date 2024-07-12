from aws_lambda_typing import context as context_
import importlib.util
import logging
import json
from typing import Optional
from config import settings

file_path = settings.handler.path # '/home/lambda/lambda_handler.py'
module_name = settings.handler.module_name # 'lambda_handler'

spec = importlib.util.spec_from_file_location(module_name, file_path)

if spec:
    module = importlib.util.module_from_spec(spec)
    if spec.loader:
        spec.loader.exec_module(module)
    else:
        raise Exception("Spec loader didn't initialized")
else:
    raise Exception("No 'lambda_handler.py' was found")

def invoke(event, context: Optional[context_.Context]) -> Optional[bytes]:
    try:
        response = module.lambda_handler(event, context)
        if response:
            message = json.dumps(response).encode()
            return message
    except Exception as exc:
        logging.error("Invokation error", exc_info = exc)
