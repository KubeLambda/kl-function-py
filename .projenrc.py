from projen.python import PythonProject

project = PythonProject(
    author_email="bfrankovskyi@gmail.com",
    author_name="Bogdan Frankovskyi",
    module_name="wrapper",
    name="function-python",
    version="0.1.0",
)
project.add_git_ignore(".mise.toml")
project.add_dependency("rocketmq-client-python==2.0.0")
project.add_dependency("aws-lambda-typing==2.20.0")
project.synth()
