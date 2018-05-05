import ast
import os
import collections
from operator import itemgetter

from nltk import pos_tag


fixture1 = '''
name_1 = 'abc'
thing2 = 63
__left = '1'
right__ = '2'
__both__ = '3'

def do_staff():
    pass

def make_him():
    pass

'''


def flat(_list):
    '''
        return flattened list that consists elememts of all subllists of _list

        >>> flat([(1,2), (3,4)])
        [1, 2, 3, 4]
    '''
    return sum([list(item) for item in _list], [])


def is_verb(word):
    '''
        >>> is_verb('do')
        True
        >>> is_verb('hello')
        False
    '''
    if not word:
        return False
    pos_info = pos_tag([word])
    return pos_info[0][1] == 'VB'

def get_tree_from_content(content):
    try:
        return ast.parse(content)
    except SyntaxError as e:
        print(e)

def get_filenames_by_ext(path, ext, limit):
    filenames = []
    for dirname, dirs, files in os.walk(path, topdown=True):
        for file in files:
            if file.endswith(ext):
                filenames.append(os.path.join(dirname, file))
                if len(filenames) >= limit:
                    break
    return filenames

def get_trees(path, with_filenames=False, with_file_content=False, limit=100):
    trees = []

    filenames = get_filenames_by_ext(path, '.py', limit)

    for filename in filenames:
        with open(filename, 'r', encoding='utf-8') as attempt_handler:
            main_file_content = attempt_handler.read()
        tree = get_tree_from_content(main_file_content)
        if with_filenames:
            if with_file_content:
                trees.append((filename, main_file_content, tree))
            else:
                trees.append((filename, tree))
        else:
            trees.append(tree)
    return trees


def get_all_names(tree):
    '''
        >>> get_all_names(ast.parse('a = 1\\nb = 17\\n'))
        ['a', 'b']
    '''
    return [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]

def split_snake_case_name_to_words(name):
    '''
        >>> list(split_snake_case_name_to_words('left_right'))
        ['left', 'right']
    '''
    return filter(not_not, name.split('_'))

def get_verbs_from_function_name(function_name):
    '''
        >>> list(get_verbs_from_function_name('take_this_thing'))
        ['take']
    '''
    return filter(is_verb, split_snake_case_name_to_words(function_name))

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


def get_all_words_in_tree(tree):
    '''
    >>> get_all_words_in_tree(ast.parse(fixture1))
    ['name', '1', 'thing2', 'left', 'right']

    :param tree:
    :return:
    '''
    function_names = filter(not_dunder, get_all_names(tree))
    return flat(map(split_snake_case_name_to_words, function_names))

def get_all_words_in_path(path):
    return flat(map(get_all_words_in_tree, filter(not_not, get_trees(path))))

def get_function_names_in_tree(tree):
    return [node.name.lower() for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]

def get_verbs_in_tree(tree):
    '''
    >>> get_verbs_in_tree(ast.parse(fixture1))
    ['do', 'make']
    '''
    all_functions = get_function_names_in_tree(tree)
    function_names = filter(not_dunder, all_functions)
    return flat(map(get_verbs_from_function_name, function_names))

def get_verbs_in_path(path):
    return flat(map(get_verbs_in_tree, filter(not_not, get_trees(path))))

def get_top_verbs_in_path(path, top_size=10):
    verbs = get_verbs_in_path(path)
    result = collections.Counter(verbs).most_common()
    result = sorted(result, key=itemgetter(0))
    result = sorted(result, key=itemgetter(1), reverse=True)
    result = result[:top_size]
    return result

def main():
    wds = []
    projects = [
        'django',
        'flask',
        'pyramid',
        'reddit',
        'requests',
        'sqlalchemy',
    ]
    for project in projects:
        path = os.path.join('.', project)
        wds += get_top_verbs_in_path(path)

    top_size = 200
    print('total %s words, %s unique' % (len(wds), len(set(wds))))
    for word, occurence in collections.Counter(wds).most_common(top_size):
        print(word, occurence)

if __name__ == "__main__":
    main()
