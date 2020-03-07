from .. import MySQLDatabaseTools
#from ..MySQLDatabaseTools import MySQLDatabase

tasks_table_name = 'tasks'
is_used_adding = '_use_column'


def check_or_create_params(params, valuable_params):
    db = MySQLDatabaseTools.get_db_worker_instance()

    if not db.table_exist(tasks_table_name):
        db.create_table(tasks_table_name, {}, pk=MySQLDatabaseTools.id_field_name)

    columns = db.get_table_columns(tasks_table_name)

    new_keys = {}

    for key in params.keys():
        if not (key in columns):
            new_keys[key] = type(params[key]) if valuable_params else params[key]

    db.add_table_columns(tasks_table_name, new_keys)

    if not check_tasks_columns():
        raise Exception("Build columns is bad!")


def check_tasks_columns():
    db = MySQLDatabaseTools.get_db_worker_instance()

    if not db.table_exist(tasks_table_name):
        return True

    columns = db.get_table_columns(tasks_table_name)
    columns.remove(MySQLDatabaseTools.id_field_name)

    for column in columns:
        if not ((column + is_used_adding) in columns):
            if not (column.replace(is_used_adding, '', 1) in columns):
                return False
    return True


