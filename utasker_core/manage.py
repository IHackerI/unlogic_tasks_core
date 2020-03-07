from .Workers import CommandsManager
import json
import sys

def main(args):
    if len(args) < 1:
        args = ["-h"]

    ans = CommandsManager.parse_commands(args, CommandsManager)

    if not (type(ans) is dict):
        ans = {"error": "ans not dict!", "ans": str(ans)}

    #MySQLDatabaseTools.close_all_connections()

    return ans


if __name__ == "__main__":
    argv = sys.argv
    argv.pop(0)
    print(json.dumps(main(argv)))
