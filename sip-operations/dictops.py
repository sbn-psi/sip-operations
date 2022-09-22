import typing

def join_dict_lists(list1, list2, join_column):
    list2_index = index_dict_list(list2, join_column)
    return(merge_dicts(dict1, list2_index[dict1[join_column]]) for dict1 in list1)

def patch_dict_list(dictlist:typing.List[typing.Dict], src_column:str, dest_column, function:typing.Callable):
    return (patch_dict(entry, src_column, dest_column, function) for entry in dictlist)

def patch_dict(entry:typing.Dict, src_column:str, dest_column:str, function:typing.Callable):
    result = entry.copy()
    replacement = function(entry[src_column])
    if replacement:
        result[dest_column] = function(entry[src_column])
    return result

def merge_dicts(dict1, dict2):
    result = {}
    result.update(dict1)
    result.update(dict2)
    return result

    
def index_dict_list(dict_list, column):
    return dict((entry[column], entry) for entry in dict_list)

def dictify_file(filename, columns):
    return (dictify_line(line, columns) for line in open(filename))

def dictify_line(line, columns):
    return dict(zip(columns, tokenize(line)))

def tokenize(line):
    return [token.strip() for token in line.split()]
