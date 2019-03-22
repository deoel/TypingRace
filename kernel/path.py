import os 

class Path:
    def __init__(self):
        pass
    
    def get_path(self, path_start, back_times, path_to_join):
        dir_path = os.path.dirname(os.path.realpath(path_start))
        for _ in range(back_times):
            dir_path = os.path.dirname(dir_path)
        complete_path = os.path.join(dir_path, path_to_join)
        return complete_path