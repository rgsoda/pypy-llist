import sys

if sys.version_info[0] == 2:
    import __builtin__

    cmp = __builtin__.cmp
    range = __builtin__.range
    xrange = __builtin__.xrange

elif sys.version_info[0] == 3:
    import builtins

    def cmp(a, b):
        return (a > b) - (a < b)

    def range(*args):
        return list(builtins.range(*args))

    xrange = builtins.range

else:
    raise NotImplemented("Only python 2 and 3 are supported")
