from redis import Redis
from rq import Queue, get_current_job
import time

def test(secs):
    print('starting task')
    for i in range(secs):
        print(i)
        time.sleep(1)
    print('task done')


def _set_task_progress(progress):
    job = get_current_job()
    if job:
        job.meta['progress'] = progress
        job.save_meta()
        #TODO


def _get_task_progress(task_id):
    #TODO
    pass


def launch_task(name, *args, **kwargs):
    q = Queue(connection=Redis(host='redis', port=6379))
    job = q.enqueue('app.tasks.' + name, *args, **kwargs)
    return job


def extract_frames():
    job = get_current_job()
    if job:
        pass

