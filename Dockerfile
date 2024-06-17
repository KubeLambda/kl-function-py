FROM python:3.9.19-slim as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends wget gcc && \
    wget https://github.com/apache/rocketmq-client-cpp/releases/download/2.0.0/rocketmq-client-cpp-2.0.0.amd64.deb
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir wheels -r requirements.txt

FROM python:3.9.19-slim

WORKDIR /home/lambda

COPY --from=builder /wheels /wheels
COPY --from=builder /requirements.txt /requirements.txt
COPY --from=builder rocketmq-client-cpp-2.0.0.amd64.deb rocketmq-client-cpp-2.0.0.amd64.deb

RUN  dpkg -i rocketmq-client-cpp-2.0.0.amd64.deb && rm rocketmq-client-cpp-2.0.0.amd64.deb && pip install --no-cache /wheels/*

# inject lambda code
ONBUILD ADD . .

COPY wrapper wrapper

CMD ["python", "wrapper"]
