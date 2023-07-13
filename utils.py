import os
import time


def cleanup(folder_path: str):
    """ Deletes all files from a folder. """
    if not os.path.exists(folder_path):
        return

    for path in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, path)):
            os.remove(os.path.join(folder_path, path))


def timeit(text):
    """ Decorator for measuring the execution time. """
    def decorator(func):
        def innerFunc(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            print(f"{text} {round(time.time() - start, 2)}")
            return result
        
        return innerFunc
    return decorator