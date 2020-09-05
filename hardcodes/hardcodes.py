#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def _gen_config(lang):
    """
    generate config for tokenization
    returns tuple
    """
    comment_strings = [
        # multi line comments
        {'start': '(*', 'end': '*)', 'langs': ['pascal', 'applescript']},
        {'start': '/*', 'end': '*/', 'langs': ['c', 'c++', 'c#', 'java', 'javascript', 'swift', 'scala', 'golang']},
        {'start': '{-', 'end': '-}', 'langs': ['haskell']},
        {'start': '\n=', 'end': '\n=', 'langs': ['perl', 'ruby']},
        {'start': '"""', 'end': '"""', 'langs': ['python']},
        {'start': '<!--', 'end': '-->', 'langs': ['xml', 'html', 'coldfusion']},
        {'start': '--[[', 'end': '--]]', 'langs': ['lua']},
        {'start': '<#', 'end': '#>', 'langs': ['php', 'powershell']},
        {'start': '\'\'\'', 'end': '\'\'\'', 'langs': ['python']},
        {'start': '<%--', 'end': '--%>', 'langs': ['jsp']},
        # single line comments
        {'start': '--', 'end': '\n', 'langs': ['ada', 'lua', 'applescript', 'sql']},
        {'start': '#', 'end': '\n', 'langs': ['php', 'perl', 'python', 'powershell']},
        {'start': '//', 'end': '\n', 'langs': ['c', 'c#', 'c++', 'java', 'javascript', 'pascal', 'php', 'scala', 'swift', 'golang']},
        {'start': '{ ', 'end': ' }', 'langs': ['pascal']}
    ]
    local_comment_strings = {}
    local_containers = ['\'', '"']

    if lang != 'common':
        for each in comment_strings:
            if lang in each['langs']:
                local_comment_strings[each['start']] = each['end']
    else:
        for each in comment_strings:
            if each['start'] not in ('{ ', '\n=', '(*'):
                local_comment_strings[each['start']] = each['end']
    return local_containers, local_comment_strings


def _is_escaped(string):
    """
    checks if given string can escape a suffix
    returns bool
    """
    count = 0
    for char in reversed(string):
        if char == '\\':
            count += 1
        else:
            break
    return count % 2


def _if_comment_started(string, comment_strings):
    """
    checks if given string starts a comment
    returns string required to close the comment and length of string that started the comment
    returns False on failure
    """
    for comment_start, comment_end in comment_strings.items():
        if string.startswith(comment_start):
            return (comment_end, len(comment_start))


def _tokenize(code, comments, comment_strings, containers):
    """
    tokenizes sources code to find hardcoded strings
    returns list of hardcoded strings
    """
    string = container = comment_end = ''
    state = 'look'
    skip = 0
    comment = False
    all_strings = []
    for index, char in enumerate(code):
        if skip > 0:
            skip -= 1
            continue
        buff = code[index:index+4]
        if comment:
            if buff.startswith(comment_end):
                skip = len(comment_end)
                if comments == 'string' and string:
                    all_strings.append(string)
                state = 'look'
                comment = False
                string = container = ''
                continue
        elif not comment and state == 'look':
            started = _if_comment_started(buff, comment_strings)
            if started:
                string = ''
                state = 'look'
                comment = True
                comment_end = started[0]
                skip = started[1] - 1
                continue
        if comment:
            if comments == 'string':
                string += char
                continue
            elif comments == 'ignore':
                continue
        if char in containers:
            if state == 'look':
                state = 'store'
                container = char
            elif state == 'store' and char == container and not _is_escaped(code[:index]):
                if string:
                    all_strings.append(string)
                string = ''
                state = 'look'
            else:
                string += char
        elif state == 'store':
            string += char
    return all_strings


def search(code, lang='common', comments='parse'):
    """
    main function that calls other functions
    returns list of hardcoded strings
    """
    containers, comment_strings = _gen_config(lang)
    return _tokenize(code, comments, comment_strings, containers)
