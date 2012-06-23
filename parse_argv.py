# parse command line arguments for use as function arguments
def for_func(function):
    from sys import argv
    import json
    f = function.func_code
    defaults = function.func_defaults
    nargs = f.co_argcount
    args = []
    kwargs = {}
    for n in range(nargs):
        name = f.co_varnames[n]
        m = n + len(defaults) - nargs
        if m < 0: # has no default value
            # obtain from argv
            try: args.append(argv[n+1])
            except IndexError: args.append(None)
        else: # has a default value
            value = defaults[m]
            if len(argv) > 1+n and not argv[1+n].startswith('--'):
                value = argv[1+n]
                kwargs[name] = value
            for arg in argv[1:]: # not the most efficient
                if arg.startswith('--'+name):
                    if '=' in arg:
                        value = arg.split('=')[1]
                        try: value = json.loads(value)
                        except ValueError: pass
                    else: value = True
            kwargs[name] = value
            if value == defaults[m]: kwargs.pop(name) # don't bother transmitting defaults
    return args,kwargs

