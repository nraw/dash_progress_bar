import time

import state_tasks as tasks

t = tasks.task.s().delay()

while not t.ready():
    print(f"State={t.state}, info={t.info}")
    time.sleep(1)

print(f"State={t.state}, info={t.info}")
