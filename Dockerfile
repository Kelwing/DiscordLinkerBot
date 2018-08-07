FROM python:3.6-alpine
WORKDIR /opt/bot
COPY requirements.txt requirements.txt
RUN apk update \
    && apk add git \
    && pip install -r requirements.txt
COPY . .
ENTRYPOINT ["python", "main.py"]
