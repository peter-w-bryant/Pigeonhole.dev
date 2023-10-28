FROM alpine:latest
WORKDIR /app
COPY . .

RUN apk add --no-cache --virtual .build-deps g++ python3-dev libffi-dev openssl-dev && \
    apk add --no-cache --update python3 py3-pip
RUN pip3 install -r requirements.txt
RUN pip3 install PyGithub

EXPOSE 5000
WORKDIR /app
CMD ["python3", "run.py", "--host", "0.0.0.0"]