from ...System import MySQLDatabaseTools
from . import Tools
from .. import Models


def save_task(task):
    db = MySQLDatabaseTools.get_db_worker_instance()

    save_params = dict(task)

    old_keys = list(save_params.keys())

    for key in old_keys:
        if key == MySQLDatabaseTools.id_field_name:
            continue
        save_params[key + Tools.is_used_adding] = True

    new_task = False

    if not (MySQLDatabaseTools.id_field_name in save_params):
        new_task = True

    Tools.check_or_create_params(save_params, True)

    if new_task:
        id_ans = db.add_data(Tools.tasks_table_name, save_params, pk=MySQLDatabaseTools.id_field_name)[0]
        task[MySQLDatabaseTools.id_field_name] = id_ans
        save_params[MySQLDatabaseTools.id_field_name] = id_ans
        save_params[Models.history_column] = task[Models.history_column]
        
    db.upd_data(Tools.tasks_table_name, save_params, pk=MySQLDatabaseTools.id_field_name)

    Tools.check_tasks_columns()

    # if not (MySQLDatabaseTools.id_field_name in save_params):
    #     save_params[MySQLDatabaseTools.id_field_name] = -1
