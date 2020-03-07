from ...System.DBTasksWork import TasksReader


def get_my_commands():
    return ["-a", "--all"]


def get_addition_info():
    return "this module read all tasks from DB"


def work(args):
    return {"ans":TasksReader.get_all_tasks()}