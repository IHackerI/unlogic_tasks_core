from .DBTasksWork import TasksSaver
from time_tools import TimeTools

history_column = 'task_history'

class Task(dict):
    def __init__(self, start_params={}):
        self.freese_history = True
        for key in start_params.keys():
            self.__setitem__(key, start_params[key])
        self.freese_history = False

    def __getitem__(self, index):
        return dict.__getitem__(self, index)

    def __setitem__(self, index, item):
        #---------------History---------------------------
        if not self.freese_history:
            if not (history_column in self):
                dict.__setitem__(self, history_column, '')

            print('history change')
            cur_history = dict.__getitem__(self, history_column)
            cur_history += str(TimeTools.get_full_now_time()) + ": new value for: `" + str(index) + "` value: " + str(item) + "\r\n"
            dict.__setitem__(self, history_column, cur_history)
        #--------------------------------------------------

        dict.__setitem__(self, index, item)

    def save(self):
        TasksSaver.save_task(self)

    def __repr__(self):
        return dict.__repr__(self)

    def __str__(self):
        return dict.__str__(self)