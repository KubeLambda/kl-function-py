from aws_lambda_typing import context as context_
import importlib.util
import logging
import json
from typing import Any, Optional
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

def invoke(event: Any, context: Optional[context_.Context]) -> Optional[bytes]:
    event_obj = event
    if type(event) is str:
        event_obj = json.loads(event)
    try:
        response = module.lambda_handler(event_obj, context)
        if response:
            message = json.dumps(response).encode()
            return message
    except Exception as exc:
        logging.exception("Invokation error", exc_info = exc)
