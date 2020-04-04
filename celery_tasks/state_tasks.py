import time

from celery import Celery

#  app = Celery("tasks", backend="rpc://", broker="pyamqp://guest@localhost//")
app = Celery("tasks")
app.config_from_object("celery_tasks.celeryconfig")


@app.task(bind=True)
def task(self):
    n = 10
    for i in range(0, n):
        update_progress(self, i, n)
        time.sleep(1)

    return n


def update_progress(tasko, i, n):
    tasko.update_state(state="PROGRESS", meta={"done": i, "total": n})
