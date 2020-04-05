from multiprocessing import Queue, Pool
import os
import time


def worker(queue_):
    pid = os.getpid()
    while True:
        item = queue_.get(block=True)

        if item == -1:
            break

        print('[process -> {}] val = {}'.format(pid, item))
        time.sleep(1)

if __name__ == '__main__':
    queue = Queue()
    pool = Pool(4, worker, (queue, ))

    # Populate the queue
    for i in range(60):
        queue.put(i)

    # Put sentinel values
    for i in range(4):
        queue.put(-1)

    pool.close()
    pool.join()