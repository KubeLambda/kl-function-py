from projen.python import PythonProject

project = PythonProject(
    author_email="bfrankovskyi@gmail.com",
    author_name="Bogdan Frankovskyi",
    module_name="function_python",
    name="function-python",
    version="0.1.0",
)

project.synth()