import os


def not_not(value):
    return not not value

def not_dunder(name):
    '''
        >>> not_dunder('value')
        True
        >>> not_dunder('__value')
        True
        >>> not_dunder('value__')
        True
        >>> not_dunder('__value__')
        False
    '''
    return not (name.startswith('__') and name.endswith('__'))

def is_python(filename):
    return filename.endswith('.py')

def get_filenames_from_path(path):
    for dirname, dirs, files in os.walk(path, topdown=True):
        for filename in files:
            yield os.path.join(dirname, filename)