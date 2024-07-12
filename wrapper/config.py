from dynaconf import Dynaconf, Validator

settings = Dynaconf(
    envvar_prefix="PYFUNC",
    settings_files=['./wrapper/settings.yaml', './wrapper/.secrets.yaml'],
    validators=[
        Validator('HANDLER', must_exist=True),
        Validator('HANDLER.path', must_exist=True),
        Validator('HANDLER.module_name', must_exist=True),
        Validator('BROKER', must_exist=True),
        Validator('BROKER.servers', must_exist=True),
        Validator('REQUEST_SUBJECT', must_exist=True),
        Validator('RESPONSE_SUBJECT_PREFIX', must_exist=True),
        Validator('TASKS_TERMINATION_TIMEOUT', must_exist=True),
    ]
)
# print(settings.as_dict())

# `envvar_prefix` = export envvars with `export PYFUNC_FOO=bar`.
# `settings_files` = Load these files in the order.
