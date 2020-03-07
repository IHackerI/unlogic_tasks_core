from inspect import getmembers, isfunction
from . import CommandsManager


def get_my_commands():
    return ["-h", "--help"]


def get_addition_info():
    return "this is HELP! set arg 'sys' for parsable answer. set arg 'full' for view full tree."


def get_addition_info_in_module(module):
    members = getmembers(module)

    for member in members:
        if isfunction(member[1]) and member[0] == "get_addition_info" and member[1].__code__.co_argcount < 1:
            return module.get_addition_info()

    return ""


def get_commands_from_object(in_module):
    ans = {}

    modules = CommandsManager.get_workers_from_module(in_module)

    for module in modules:
        ans[module.__name__] = [CommandsManager.get_call_commands_in_module(module),
                                get_addition_info_in_module(module),
                                get_commands_from_object(module) if CommandsManager.module_is_package(module) else {}
                                ]

    return ans

def print_help_to_screen(module_help, level_tabs, full_tree):
    for key in module_help.keys():

        print(level_tabs + "\t".join(module_help[key][0]) + "\t\t" + str(module_help[key][1]))

        if full_tree: 
            print_help_to_screen(module_help[key][2], level_tabs+"\t", full_tree)

def work(args, parent_module):
    ans = get_commands_from_object(parent_module)
    if len(args) > 0 and ("sys" in args):
        return {"ans": ans }

    print_help_to_screen(ans, '', ("full" in args))

    return {}
