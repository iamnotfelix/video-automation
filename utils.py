from functools import wraps
import os
import time


def cleanup(folder_path: str):
    '''
        Deletes all files from a folder.
    '''
    if not os.path.exists(folder_path):
        return

    for path in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, path)):
            os.remove(os.path.join(folder_path, path))


def timeit(func):
    '''
        Decorator for measuring the execution time.
    '''
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__}: {total_time:.4f}s')
        return result
    return timeit_wrapper