FROM python:3.6-alpine
WORKDIR /opt/bot
COPY . .
RUN apk update \
    && apk install git \
    && pip install -r requirements.txt
ENTRYPOINT ["python", "main.py"]