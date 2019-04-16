FROM python:3.6-slim

WORKDIR /app
COPY . /app

RUN pip3 install pipenv && pipenv install --deploy --system

CMD ["python3", "main.py"]