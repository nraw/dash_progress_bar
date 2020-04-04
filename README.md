# Progress bar

## Installation

You'll need:

- celery for the task
- rabbitmq for the messaging service

You can get rabbitmq running in docker with:

```
docker run -d -p 5672:5672 rabbitmq
```

also,

```
pip install -r requirements.txt
```

## Running

Assuming you already have rabbitmq running.

Start the celery task queue:

```
celery -A celery_tasks.state_tasks worker --loglevel=info
```

and start the app

```
python3 app.py
```
