import importlib
import os
import pkgutil
from inspect import getmembers, isfunction
from . import Helper

def get_addition_info():
    return "this is main enter point. Call any command!"


def get_call_commands_in_module(module):
    members = getmembers(module)

    for member in members:
        if isfunction(member[1]) and member[0] == "get_my_commands" and member[1].__code__.co_argcount < 1:
            return module.get_my_commands()

    return []


def call_work_module(base_mod, parent_mod, args):
    members = getmembers(base_mod)

    for member in members:
        if isfunction(member[1]) and member[0] == "work":
            args_count = member[1].__code__.co_argcount
            if args_count < 3:
                if args_count == 2:
                    return base_mod.work(args, parent_mod)
                elif args_count == 1:
                    return base_mod.work(args)
                else:
                    return base_mod.work()

    return {"error": "module not contain work function!", "module": base_mod}


def command_finder(base_module, parent_mod, args):
    if len(args) < 1 or len(args[0]) < 1 or args[0][0] != '-':
        return call_work_module(base_module, parent_mod, args)

    mods = get_workers_from_module(base_module)

    command = args.pop(0).lower()

    for mod in mods:
        commands = get_call_commands_in_module(mod)
        if command in commands:
            return command_finder(mod, base_module, args)

    return {"error": "command not found!", "command": command}


def module_is_package(module):
    dir_name = os.path.dirname(module.__file__)
    folds = dir_name.replace('\\', '/').split('/')
    name_split = module.__name__.split('.')
    if folds[len(folds) - 1] != name_split[len(name_split) - 1]:
        return False
    return True


def get_workers_from_module(module):
    modules = []

    dir_name = os.path.dirname(module.__file__)
    path = module.__name__

    if not module_is_package(module):
        path = path.split('.')
        path.pop(len(path)-1)
        path = '.'.join(path)

    for loader, name, is_pkg in pkgutil.walk_packages([dir_name]):
        modules.append(importlib.import_module(path + "." + name))

    if not (Helper in modules):
        modules.append(Helper)

    return modules


def parse_commands(args, base_worker):
    return command_finder(base_worker, None, args)


def work(args, parent_module):
    return {"error": "not one commands found! call -h for help!", "args": args, "pm": parent_module}
