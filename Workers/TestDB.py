#from ..System.MySQLDatabaseTools import MySQLDatabase
#from ..System import MySQLDatabaseTools
from ..System.Models import Task


def get_my_commands():
    return ["-tdb", "--testdb"]


def get_addition_info():
    return "this module test db!"


def work(args):
    return {"ans": "dbTest"}
    from ..System.DBTasksWork import TasksReader
    t_dict = {}

    #t_dict["id"] = "olol"

    # db = MySQLDatabaseTools.get_db_worker_instance()

    # columns = db.get_table_columns('autotestTable', True)

    all_tasks = TasksReader.get_all_tasks()

    save_task = Task()

    # save_task["olol_column"] = "any_value"
    save_task["third"] = "VALUE"

    all_tasks[0]["chetyire"] = 50

    save_task.save()
    all_tasks[0].save()

    return save_task



    if not db.table_exist('autotestTable'):
        db.create_table('autotestTable', {'testColumn': str, 'intTestColumn' : int}, pk='ololid')

    db.add_data('autotestTable', {'testColumn': 'forView', 'intTestColumn': 5}, pk='ololid')

    rows = db.get_all_rows('autotestTable')

    return rows
