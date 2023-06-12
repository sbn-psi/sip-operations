import typing

def join_dict_lists(list1, list2, join_column):
    '''Performs an operation like a SQL equijoin on two tables, which are represented as dictionary lists.'''
    list2_index = index_dict_list(list2, join_column)
    return(merge_dicts(dict1, list2_index[dict1[join_column]]) for dict1 in list1)

def patch_dict_list(dictlist:typing.List[typing.Dict], src_column:str, dest_column, function:typing.Callable):
    '''Replaces all of the values for a specified key in a table (dictionary list) with the result of a function'''
    return (patch_dict(entry, src_column, dest_column, function) for entry in dictlist)

def patch_dict(entry:typing.Dict, src_column:str, dest_column:str, function:typing.Callable):
    '''Replaces the values for a specified key in a dictionary with the result of a function'''
    result = entry.copy()
    replacement = function(entry[src_column])
    if replacement:
        result[dest_column] = function(entry[src_column])
    return result

def merge_dicts(dict1, dict2):
    '''Combines two dictionaries with a single dictionary. If both dictionaries contain the same key, dict2 takes precedence'''
    result = {}
    result.update(dict1)
    result.update(dict2)
    return result

    
def index_dict_list(dict_list, column):
    '''Creates a structure like a SQL index for fast access to a specific row (dict) in a table (dict list)'''
    return dict((entry[column], entry) for entry in dict_list)

def dictify_file(filename, columns):
    '''Converts a structured text file into a table (dict list)'''
    return (dictify_line(line, columns) for line in open(filename))

def dictify_line(line, columns):
    '''Converts a line in a structured text file into a record (dict)'''
    return dict(zip(columns, tokenize(line)))

def tokenize(line):
    '''Splits a line into a list of tokens'''
    return [token.strip() for token in line.split()]
