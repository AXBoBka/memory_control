# syntax=docker/dockerfile:1.4
FROM python:3.10-alpine AS deploy

WORKDIR /src
COPY requirements.txt /src
RUN apk add --update --no-cache g++ gcc musl-dev linux-headers
RUN pip install -r requirements.txt

COPY . .

RUN adduser -D user
USER user

CMD ["sh", "-c", ". .env; python3 memory_control.py ./config/config.json 10"]
