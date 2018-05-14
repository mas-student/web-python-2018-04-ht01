import os
import collections
from operator import itemgetter

from .helpers import is_python, get_filenames_from_path
from .parse import get_tree_from_filename, get_nodes_from_trees, get_words_from_names, is_function_node, get_node_name
from .analysis import is_verb


def get_top_function_name_verbs_in_path(path, top_size=10):
    trees = map(get_tree_from_filename, filter(is_python, get_filenames_from_path(path)))
    function_names = map(get_node_name, filter(is_function_node, get_nodes_from_trees(trees)))
    verbs = filter(is_verb, get_words_from_names(function_names))

    return collections.Counter(verbs).most_common(top_size)

def main():
    '''
    >>> main()
    None
    '''
    projects = [
        'django',
        'flask',
        'pyramid',
        'reddit',
        'requests',
        'sqlalchemy',
    ]
    total_top_verbs = []
    for project in projects:
        path = os.path.join('..', project)

        top_verbs = get_top_function_name_verbs_in_path(path)
        total_top_verbs += top_verbs

    top_size = 200
    print('total %s words, %s unique' % (len(total_top_verbs), len(set(total_top_verbs))))
    for word, occurence in collections.Counter(total_top_verbs).most_common(top_size):
        print(word, occurence)

if __name__ == "__main__":
    main()
