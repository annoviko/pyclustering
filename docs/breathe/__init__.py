
__version__ = '3.2.0'


def setup(app):

    # We can't do the import at the module scope as setup.py has to be able to
    # import this file to read __version__ without hitting any syntax errors
    # from both Python 2 & Python 3.

    # By the time this function is called, the directives code will have been
    # converted with 2to3 if appropriate

    from . import directives

    directives.setup(app)
