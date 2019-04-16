# census-rm-case-processor-prototype-python

A service that does the following:

- Consumes messages from a rabbit queue
- Runs some business logic based on the type of message (such as creating a case)
- Emits an message to a rabbit queue to allow other services to react to the event

## Prerequisities

- PostgresSQL (default: instance running locally on port 6432)
- RabbitMQ (default: instance running locally on port 6672)
- pyenv

## Setup

Install dependencies:
```
pyenv install
pip install pipenv
pipenv install --dev
```

Run application:

```
DEV=True pipenv run python main.py 
```