from threading import Thread, Lock
from queue import Queue
import logging
import time
from server.config import interval

logger = logging.getLogger()


class Worker(Thread):
    """ Thread executing tasks from a given tasks queue """
    def __init__(self, tasks, workers, tid):
        Thread.__init__(self)
        self.tasks = tasks
        self.workers = workers
        self.tid = tid
        self.lock = Lock()
        self.start()

    def run(self):
        while True:
            error = False
            func = None
            args = None
            kwargs = None
            try:
                func, args, kwargs = self.tasks.get()
                func(*args, **kwargs)
            except Exception as e:
                # An exception happened in this thread
                print(e)
                logger.info(e)
                error = True
            finally:
                if error:
                    if func:
                        self.tasks.put((func, args, kwargs))

                    self.lock.acquire()
                    self.workers[self.tid] = None
                    self.lock.release()
                    break


class WorkerDaemon(Thread):
    """ Thread executing tasks from a given tasks queue """
    def __init__(self, task_queues, workers, interval=10):
        Thread.__init__(self)
        self.workers = workers
        self.task_queues = task_queues
        self.interval = interval
        self.daemon = True
        self.lock = Lock()
        self.start()

    def run(self):
        while True:
            self.lock.acquire()
            try:
                for key, value in self.workers.items():
                    if value is None:
                        worker = Worker(self.task_queues[key], self.workers, key)
                        self.workers[key] = worker

            except Exception as e:
                # An exception happened in this thread
                print(e)
                logger.info(e)
            finally:
                self.lock.release()
                time.sleep(self.interval)


class ThreadPool:
    """ Pool of threads consuming tasks from a queue """
    def __init__(self, num_threads):
        self.lock = Lock()
        self.task_queues = {}
        self.workers = {}
        self.lock.acquire()
        for i in range(num_threads):
            queue = Queue()
            self.task_queues[i] = queue
            worker = Worker(queue, self.workers, i)
            self.workers[i] = worker
        WorkerDaemon(self.task_queues, self.workers, interval=interval)
        self.lock.release()

    def add_task(self, tid, func, *args, **kargs):
        """ Add a task to the queue """
        self.task_queues[tid].put((func, args, kargs))

    def map(self, tid, func, args_list):
        """ Add a list of tasks to the queue """
        for args in args_list:
            self.add_task(tid, func, args)
