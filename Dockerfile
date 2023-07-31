FROM python:3.10
EXPOSE 5000
WORKDIR /app
COPY /backend .

RUN pip install -r requirements.txt

WORKDIR /app/api
CMD ["python3", "app.py", "--host", "0.0.0.0"]