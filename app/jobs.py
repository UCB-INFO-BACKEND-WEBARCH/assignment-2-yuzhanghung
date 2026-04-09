import time

def notify_task_created(name):
    print(f"Starting job for {name}")
    time.sleep(5)
    print(f"Finished job for {name}")