from ...System import MySQLDatabaseTools
from . import Tools
from ...System.Models import Task


def raw_tasks_to_tasks(raw_tasks):
    if raw_tasks is None:
        return []

    ans_tasks = []

    for row in raw_tasks[1]:
        cur_tsk = None
        cur_tsk = Task()
        cur_tsk.freese_history = True
        for idx, col_value in enumerate(row):
            if raw_tasks[0][idx] == MySQLDatabaseTools.id_field_name:
                cur_tsk[MySQLDatabaseTools.id_field_name] = col_value
                continue
            use_column_name = raw_tasks[0][idx]+Tools.is_used_adding
            try:
                use_column_index = raw_tasks[0].index(use_column_name)
            except ValueError:
                use_column_index = -1
            if use_column_index < 0 or (not row[use_column_index]):
                continue
            cur_tsk[raw_tasks[0][idx]] = col_value
        #print(str(cur_tsk["id"]))
        cur_tsk.freese_history = False
        ans_tasks.append(cur_tsk)

    return ans_tasks


def get_task(task_id):
    db = MySQLDatabaseTools.get_db_worker_instance()
    # TODO fix SQL injection!
    raw_tasks = db.get_rows_where(Tools.tasks_table_name, "`" + MySQLDatabaseTools.id_field_name + "` = '" + str(task_id)+"'")

    ans = raw_tasks_to_tasks(raw_tasks)

    return ans[0] if len(ans) > 0 else None


def get_tasks_where(logic):
    db = MySQLDatabaseTools.get_db_worker_instance()
    # TODO fix SQL injection!
    raw_tasks = db.get_rows_where(Tools.tasks_table_name, logic)
    return raw_tasks_to_tasks(raw_tasks)


def get_all_tasks():
    db = MySQLDatabaseTools.get_db_worker_instance()
    raw_tasks = db.get_all_rows(Tools.tasks_table_name)
    return raw_tasks_to_tasks(raw_tasks)

