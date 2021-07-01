from multiprocessing.pool import ThreadPool
import shutil


class MultiThreadCopier:
    def __init__(self, threads):
        self.pool = ThreadPool(threads)

    def copy(self, src, dst):
        self.pool.starmap(shutil.copy2, [(src, dst)])

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pool.close()
        self.pool.join()
