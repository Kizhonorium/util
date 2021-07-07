from multiprocessing.pool import ThreadPool
import shutil
import os
import logging


class MultiThreadCopier:
    def __init__(self, threads):
        self.pool = ThreadPool(threads)

    def copy(self, src, dst):
        """ Copy the file from src to dst using shutil.copy2 """
        self.pool.starmap(shutil.copy2, [(src, dst)])

    def copy_tree(self, src, dst):
        """ Copy the directory from src to dst  """
        for root, dirs, files in os.walk(src):
            dst_dir = root.replace(src, dst, 1)
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)
            for file in files:
                src_file = os.path.join(root, file)
                dst_file = os.path.join(dst_dir, file)
                if os.path.exists(dst_file):
                    os.remove(dst_file)
                self.copy(src_file, dst_dir)

    def copy_file_by_extension(self, src, dst, copy_function=None):
        """ Copy file by extension from src to dst """
        for file in self.list_files_by_extension(src):
            if os.path.isfile(file):
                if copy_function:
                    try:
                        shutil.move(file, dst, copy_function)
                    except shutil.Error as e:
                        logging.error("Destination path '%s' already exists" % file)
                else:
                    self.copy(file, dst)

    def list_files_by_extension(self, _path):
        """ Get a list of all files in a directory """
        if self.is_dir(_path):
            return os.listdir(_path)

        return [os.path.join(root, file) 
            for root, dirs, files in os.walk(os.path.dirname(_path))
            for file in files 
            if file.endswith(os.path.basename(_path))
        ]

    def is_dir(self, _path):
        return os.path.isdir(os.path.basename(_path))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pool.close()
        self.pool.join()
