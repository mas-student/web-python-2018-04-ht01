from nltk import pos_tag

from .parse import split_snake_case_name_to_words


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
    return pos_info[0][1] in ['VB', 'VBZ', 'VBP']

def starts_with_verb(name):
    '''
        >>> starts_with_verb('make_staff')
        True
        >>> starts_with_verb('one_staff')
        False
    '''
    return is_verb(list(split_snake_case_name_to_words(name))[0])

def not_starts_with_verb(name):
    return not starts_with_verb(name)
