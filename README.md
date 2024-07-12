# Python Function

Wrap lambda code with python for serverless project
It wraps docker build of the python code and execute it. For example take a look into [Dockerfile](./example/example_lambda/Dockerfile)
Project uses [projen](./.projenrc.py) for housekeeping

## Install

```sh 
npx projen
pip install -r requirements.txt
```

## Build with example code

```sh
docker build -q example/example_lambda/
```

## Configuration

Can be configured by env variables. See [dynaconf](https://www.dynaconf.com) and [settings](./wrapper/settings.yaml)

