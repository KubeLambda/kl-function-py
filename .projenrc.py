from projen import ProjectType
from projen.python import PythonProject

author_name = "Bohdan Frankovskyi"
license_spdx = "Apache-2.0"

project = PythonProject(
    author_email="bfrankovskyi@gmail.com",
    author_name=author_name,
    module_name="wrapper",
    name="kl_function_py",
    description="KubeLambda python function",
    license=license_spdx,
    version="0.1.0",
    github=True,
    project_type=ProjectType.APP,
    poetry=False,
    pytest=False,
)
project.add_git_ignore(".mise.toml")
project.add_git_ignore(".secrets.yaml")
project.add_git_ignore("!/LICENSE")
project.add_dependency("nats-py==2.8.0")
project.add_dependency("aws-lambda-typing==2.20.0")
project.add_dependency("dynaconf==3.2.5")

# License(project, spdx=license_spdx, copyright_owner=author_name).synthesize()

project.synth()
