FROM python:3.9.19-slim as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir wheels -r requirements.txt

FROM python:3.9.19-slim

WORKDIR /home/lambda

COPY --from=builder /wheels /wheels
COPY --from=builder /requirements.txt /requirements.txt

RUN pip install --no-cache /wheels/*

# inject lambda code
ONBUILD ADD . .

COPY wrapper wrapper

CMD ["python", "wrapper"]
