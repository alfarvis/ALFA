#!/usr/bin/env python
from PyQt5.QtCore import QThreadPool


class ThreadPoolManager(object):
    @classmethod
    def initialize(self, n_threads=3, timeout=30000):
        """
        Initialize pool
        Args:
            n_threads: Number of threads
            timeout: closes a thread if it takes more than timeout milliseconds
        """
        QThreadPool.globalInstance().setMaxThreadCount(n_threads)
        QThreadPool.globalInstance().setExpiryTimeout(timeout)

    @classmethod
    def addWorker(self, worker):
        """
        Add worker thread to the pool
        """
        QThreadPool.globalInstance().start(worker)

    @classmethod
    def close(self, timeout=1000):
        """
        Wait for timeout and cleanup all threads
        """
        pass
        # QthreadPool.globalInstance().waitForDone(timeout)
