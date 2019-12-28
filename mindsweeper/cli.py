from functools import wraps
from inspect import getfullargspec
import re

class CommandLineInterface:
    def __init__(self):
        self.func = {}

    def command(self, f):
        self.func[f.__name__] = {'func': f, 'argspec': getfullargspec(f)}
        @wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)
        return wrapper

    def main(self):
        import sys
        global argv
        argv = sys.argv
        callargs = {}
        if len(argv) < 2:
            print(f'USAGE: python example.py <command> [<key>=<value>]* \n Not enough arguments') #not enough arguments
            sys.exit(1)
        name = argv[1]
        if name not in self.func:
            print(f'USAGE: python example.py <command> [<key>=<value>]* \n Function {name} not found') #invalid function name
            sys.exit(1)
        else:
            for arg in argv[2:]:
                if not re.match('^[a-zA-Z_$][a-zA-Z_$0-9]*=[^=]*$',arg):
                #allows only valid variable names and only one equal sign. can be changed later to include strings as repr
                    print(f'USAGE: python example.py <command> [<key>=<value>]* \n One or more arguments are given in invalid format') #invalid arguments format
                    sys.exit(1)
                else:
                    arg = arg.split('=') #arg[0] for variable name, arg[1] for value
                    if arg[0] not in self.func[name]['argspec'][0] and not self.func[name]['argspec'][2]:
                    #if these are valid argument variable names, or kwargs are allowed
                        print(f'USAGE: python example.py <command> [<key>=<value>]* \n No such arguments for {name}')
                        sys.exit(1)
                    else:
                        callargs[arg[0]] = arg[1]
        self.func[name]['func'](**callargs)
