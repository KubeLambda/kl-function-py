from projen import ProjectType
from projen.python import PythonProject

project = PythonProject(
    author_email="bfrankovskyi@gmail.com",
    author_name="Bogdan Frankovskyi",
    module_name="wrapper",
    name="function-python",
    version="0.1.0",
    github=True,
    project_type=ProjectType.APP,
    poetry=False,
    pytest=False,
)
project.add_git_ignore(".mise.toml")
project.add_git_ignore(".secrets.yaml")
project.add_dependency("nats-py==2.8.0")
project.add_dependency("aws-lambda-typing==2.20.0")
project.add_dependency("dynaconf==3.2.5")
project.synth()
