import re
from ...System.Models import Task
from ...System import MySQLDatabaseTools


def get_my_commands():
    return ["-nt", "--newtask"]


def get_addition_info():
    return "this module create task for you! For my work, enter:\n" \
           "param1:value1 param2:value2 ... paramX:valueX"


def clear_titles(title):
    return re.sub('[\t\r\n]', '', title).strip()


def work(args):
    params = {}

    cur_args = list(args)

    #args.clear()

    for arg in cur_args:
        vals = arg.split(":",1)
        if len(vals) < 2:
            return "Unnamed param found! Unnamed param arg: " + str(arg)
        elif len(vals) > 2: # никогда не случится
            return "in command Symbol ':' contains more 2 times: " + str(arg)
        else:
            params[clear_titles(vals[0])] = clear_titles(vals[1])

    ans = Task(params)
    ans.save()

    return {MySQLDatabaseTools.id_field_name: ans[MySQLDatabaseTools.id_field_name]}
