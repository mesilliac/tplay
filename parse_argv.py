# parse command line arguments for use as function arguments
def for_func(function):
    from sys import argv
    import json
    f = function.func_code
    defaults = function.func_defaults
    nargs = f.co_argcount
    args = []
    kwargs = {}
    keywords = {}
    for i in xrange(1,len(argv)):
        if argv[i].startswith('--'):
            sa = argv[i][2:].split('=')
            try: keywords[sa[0]] = json.loads(sa[1])
            except ValueError: keywords[sa[0]] = sa[1]
            except IndexError: keywords[sa[0]] = True
    arguments = [x for x in argv[1:] if not x.startswith('--')]
    for n in xrange(nargs):
        name = f.co_varnames[n]
        m = n + len(defaults) - nargs
        if m < 0: # has no default value
            try: args.append(arguments[n])
            except IndexError: args.append(None)
        else: # has a default value
            if n < len(arguments): value = arguments[n]
            else: value = keywords.get(name,defaults[m])
            kwargs[name] = value
            if value == defaults[m]: kwargs.pop(name) # don't bother transmitting defaults
    return args,kwargs

