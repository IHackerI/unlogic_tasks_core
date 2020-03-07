from ...System.DBTasksWork import TasksReader


def get_my_commands():
    return ["-wh", "--where"]


def get_addition_info():
    return "this module read tasks from DB by filter"


def work(args):
    if len(args)<1:
        return {"error":"filter empty!"}
    try:
        return {"ans":TasksReader.get_tasks_where(args[0])}
    except Exception as e:
        return {"error": e }