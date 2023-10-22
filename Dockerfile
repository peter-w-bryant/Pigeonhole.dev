FROM alpine:latest
WORKDIR /app
COPY /backend .

RUN apk add --no-cache --virtual .build-deps g++ python3-dev libffi-dev openssl-dev && \
    apk add --no-cache --update python3 py3-pip
RUN pip3 install -r requirements.txt
RUN pip3 install PyGithub

# Switch directory to api
WORKDIR /app/api
RUN python3 ./scripts/populate_db.py 10

EXPOSE 5000
WORKDIR /app
CMD ["python3", "api/app.py", "--host", "0.0.0.0"]