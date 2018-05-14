import ast

from .helpers import not_not, not_dunder


def get_tree_from_content(content):
    try:
        return ast.parse(content)
    except SyntaxError as e:
        print(e), content

def get_tree_from_filename(filename, with_filenames=False, with_file_content=False):
    with open(filename, 'r', encoding='utf-8') as attempt_handler:
        main_file_content = attempt_handler.read()
    tree = get_tree_from_content(main_file_content)
    if with_filenames:
        if with_file_content:
            result = (filename, main_file_content, tree)
        else:
            result = (filename, tree)
    else:
        result = tree
    return result

def get_trees_from_filenames(filenames, with_filenames=False, with_file_content=False):
    for filename in filenames:
        element = get_tree_from_filename(filename)
        if element:
            yield element

def is_name_node(node):
    '''
        >>> list(map(get_node_id, filter(is_name_node, get_nodes_from_trees([ast.parse('a = 1\\nb = 17\\n')]))))
        ['a', 'b']
    '''
    return isinstance(node, ast.Name)

def is_function_node(node):
    return isinstance(node, ast.FunctionDef)

def get_node_name(node):
    return node.name.lower()

def get_node_id(node):
    return node.id

def get_nodes_from_trees(trees):
    '''
        >>> list(map(get_node_id, filter(is_name_node, get_nodes_from_trees([ast.parse('a = 1\\nb = 17\\n')]))))
        ['a', 'b']
    '''
    for nodes in map(ast.walk, trees):
        for node in nodes:
            if node:
                yield node

def split_snake_case_name_to_words(name):
    '''
        >>> list(split_snake_case_name_to_words('left_right'))
        ['left', 'right']
        >>> list(split_snake_case_name_to_words('name_1'))
        ['name', '1']
        >>> list(split_snake_case_name_to_words('getValue'))
        ['getValue']
    '''
    return filter(not_not, name.split('_'))


def get_words_from_names(names, splitter=split_snake_case_name_to_words):
    for words in map(splitter, filter(not_dunder, names)):
        for word in words:
            yield word