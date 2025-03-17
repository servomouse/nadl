from new_tokenizer import tokenize, update_ranges
import re
import json
import sys


def extract_substring(s, substring):
    start = s.find(substring)
    if start == -1:
        return None
    depth = 0
    for i in range(start + len(substring), len(s)):
        if s[i] == '[':
            depth += 1
        elif s[i] == ']':
            depth -= 1
            if depth == 0:
                return s[start:i+1]
    return None


def replace_substring(original_string, s0, s1):
    return re.sub(s0, s1, original_string)

# a = r"\w+ \d+ x \[((?:\w+\[\d+\](?:, )?|\w+\[\d+:\d+\](?:, )?)*)\]\s*type\s*\w+"

# group_description_regex = r"groups\s*:\s*\[\s*(\w+\s*\d+\s*x\s*\[(\b(?!except|exclude)\w+\b\s*\[\d+(?::\d+)?\](?:\s+(except|exclude)\s*\[\d+(?::\d+)?\])*(?:,\s*)?)+\]\s+type\s+\w+\s*(,\s*)?)+\s*\]"

# a = r"\w*\s*\d+\s*x\s*\[(\b(?!except|exclude)\w+\b\s*\[\d+(?::\d+)?\](?:\s+(except|exclude)\s*\[\d+(?::\d+)?\])*(?:,\s*)?)+\]\s+type\s+\w+\s*((,\s*)|\])"

# i_range = "\w*\s*\d+(?::\d+){0,1}\s*"
# r_inputs = f"inputs\s*:\s*\[\s*({i_range},\s*)*\s*{i_range}\]"

# group_name = "\b(?!except|exclude)\w+\b"
# g_range = "\[\d+(?::\d+)?\]"
# g_inputs = f"(\s*{group_name}\s*{g_range}(?:\s+(except|exclude)\s*{g_range})*"
# g_definition = f"(\w*\s*\d+\s*x\s*\[{g_inputs},)*{g_inputs})+\s*\]\s+type\s+\w+\s*"
# r_groups = f"groups\s*:\s*\[\s*{g_definition},\s*)*{g_definition})+\s*\]"

# # r_groups = f"groups\s*:\s*\[\s*(\w*\s*\d+\s*x\s*\[(\s*\b(?!except|exclude)\w+\b\s*\[\d+(?::\d+)?\](?:\s+(except|exclude)\s*\[\d+(?::\d+)?\])*,)*(\s*\b(?!except|exclude)\w+\b\s*\[\d+(?::\d+)?\](?:\s+(except|exclude)\s*\[\d+(?::\d+)?\])*)+\s*\]\s+type\s+\w+\s*,\s*)*(\w*\s*\d+\s*x\s*\[(\s*\b(?!except|exclude)\w+\b\s*\[\d+(?::\d+)?\](?:\s+(except|exclude)\s*\[\d+(?::\d+)?\])*,)*(\s*\b(?!except|exclude)\w+\b\s*\[\d+(?::\d+)?\](?:\s+(except|exclude)\s*\[\d+(?::\d+)?\])*)+\s*\]\s+type\s+\w+\s*)+\s*\]"

# r_outputs = f"outputs\s*:\s*\[\s*{g_definition},\s*)*{g_definition})+\s*\]"

# # r_module = r"module\s*:\s*\w+\s*((inputs\s*:\s*\[\s*(\w*\s*\d+(?::\d+){0,1}\s*,\s*)*\s*\w*\s*\d+(?::\d+){0,1}\s*\])|(groups\s*:\s*\[\s*(\w*\s*\d+\s*x\s*\[(\b(?!except|exclude)\w+\b\s*\[\d+(?::\d+)?\](?:\s+(except|exclude)\s*\[\d+(?::\d+)?\])*(?:,\s*)?)+\]\s+type\s+\w+\s*(,\s*)?)+\s*\])|(outputs\s*:\s*\[\s*(\w*\s*\d+\s*x\s*\[(\b(?!except|exclude)\w+\b\s*\[\d+(?::\d+)?\](?:\s+(except|exclude)\s*\[\d+(?::\d+)?\])*(?:,\s*)?)+\]\s+type\s+\w+\s*(,\s*)?)+\s*\]))+"

# # r_mod_new = r"(?=.*(inputs\s*:\s*\[\s*(\w*\s*\d+(?::\d+){0,1}\s*,\s*)*\s*\w*\s*\d+(?::\d+){0,1}\s*\])))(?=.*(outputs\s*:\s*\[\s*(\w*\s*\d+\s*x\s*\[(\b(?!except|exclude)\w+\b\s*\[\d+(?::\d+)?\](?:\s+(except|exclude)\s*\[\d+(?::\d+)?\])*(?:,\s*)?)+\]\s+type\s+\w+\s*(,\s*)?)+\s*\]))[(inputs\s*:\s*\[\s*(\w*\s*\d+(?::\d+){0,1}\s*,\s*)*\s*\w*\s*\d+(?::\d+){0,1}\s*\]))(outputs\s*:\s*\[\s*(\w*\s*\d+\s*x\s*\[(\b(?!except|exclude)\w+\b\s*\[\d+(?::\d+)?\](?:\s+(except|exclude)\s*\[\d+(?::\d+)?\])*(?:,\s*)?)+\]\s+type\s+\w+\s*(,\s*)?)+\s*\]))(groups\s*:\s*\[\s*(\w*\s*\d+\s*x\s*\[(\b(?!except|exclude)\w+\b\s*\[\d+(?::\d+)?\](?:\s+(except|exclude)\s*\[\d+(?::\d+)?\])*(?:,\s*)?)+\]\s+type\s+\w+\s*(,\s*)?)+\s*\])]+"

# a = r_inputs
# b = r_groups
# c = r_outputs
# r_module = f"{r_module}?(?=[{a}{c}{b}]*{a})(?=[{a}{c}{b}]*{c})[{a}{c}{b}]+"

# Throws exception if expression is False
def nadl_assert(expression, error_str, line):
    if not expression:
        raise Exception(f"Error at line {line}: {error_str}")

def prepare_data(data):
    lines = []
    counter = 0
    for line in data:
        counter += 1
        temp = line.split('#')[0]
        if len(temp) > 0:
            lines.append({
                'len': len(temp),
                'text': temp.strip(),
                'l_number': counter,
            })
    return lines


def get_module_name(tokens):
    mod_name = None
    if tokens[0]['type'] == 'keyword' and tokens[0]['val'] == 'module':
        if tokens[1]['type'] != 'colon':
            raise Exception(f"Syntax error at line {tokens[1]['l_number']}: expected \":\" after keyword \"module\"")
        if tokens[2]['type'] != 'label':
            raise Exception(f"Syntax error at line {tokens[2]['l_number']}: expected module name")
        if tokens[2]['val'] in ['except', 'exclude', 'module', 'inputs', 'groups', 'outputs', 'type']:
            raise Exception(f"Syntax error at line {tokens[2]['l_number']}: invalid module name \"{tokens[2]['val']}\"")
        mod_name = tokens[2]['val']
        tokens = tokens[3:]
    elif (tokens[0]['type'] == 'label') and (tokens[0]['val'] in ['inputs', 'outputs', 'groups']):
        mod_name = 'default'
    else:
        raise Exception(f"Syntax error at line {tokens[0]['l_number']}: start config with \"module: <module_name>\" or \"inputs:\"/\"groups:\"/\"outputs:\"")
    return mod_name, tokens


def parse_inputs(tokens):
    inputs = []
    if (tokens[0]['type'] != 'colon') or (tokens[1]['type'] != 'open_bracket'):
        raise Exception(f"Syntax error at line {tokens[0]['l_number']}: Correct syntax is as following: inputs: [...")
    tokens = tokens[2:]
    curr_name = None
    while len(tokens) > 0:
        if tokens[0]['type'] == 'range':
            r = tokens[0]['val']
            r_size = 1 if r[1] == r[0] else r[1] - r[0]
            inputs.append({'group_name': curr_name, 'group_size': r_size, 'g_range': [r[0], r[1]]})
            curr_name = None
        elif tokens[0]['type'] == 'label':
            if tokens[0]['val'] in ['except', 'exclude', 'module', 'inputs', 'groups', 'outputs', 'type']:
                raise Exception(f"Error: invalid inputs group name: {tokens[0]['val']}")
            if curr_name is not None:
                raise Exception(f"Error at line {tokens[0]['l_number']}: Unexpected label: {tokens[0]['val']}")
            curr_name = tokens[0]['val']
        elif tokens[0]['type'] == 'comma':
            pass
        elif tokens[0]['type'] == 'close_bracket':
            tokens = tokens[1:]
            break
        else:
            raise Exception(f"Error at line {tokens[0]['l_number']}: Unexpected token: \"{tokens[0]['val']}\"")
        tokens = tokens[1:]
    # print(inputs)
    return inputs, 'inputs', tokens


def parse_group_input(tokens):
    i_name = None
    i_range = None
    i_except = []
    i_exclude = []

    nadl_assert(tokens[0]['type'] == 'label', f"Unexpected label: {tokens[0]['val']}", tokens[0]['l_number'])
    nadl_assert(tokens[1]['type'] == 'open_bracket', f"Unexpected label: {tokens[1]['val']}", tokens[1]['l_number'])
    nadl_assert(tokens[2]['type'] == 'range', f"Unexpected label: {tokens[2]['val']}", tokens[2]['l_number'])
    nadl_assert(tokens[3]['type'] == 'close_bracket', f"Unexpected label: {tokens[3]['val']}", tokens[3]['l_number'])
    i_name = tokens[0]['val']
    i_range = tokens[2]['val']
    tokens = tokens[4:]
    if (tokens[0]['type'] == 'comma') or (tokens[0]['type'] == 'close_bracket'):
        return {
            'i_name': i_name,
            'i_range': i_range,
            'except': [],
            'exclude': []
        }, tokens
    while len(tokens) > 0:
        nadl_assert(tokens[0]['type'] == 'keyword', f"Unexpected label: {tokens[0]['val']}", tokens[0]['l_number'])
        nadl_assert(tokens[1]['type'] == 'open_bracket', f"Unexpected label: {tokens[1]['val']}", tokens[1]['l_number'])
        nadl_assert(tokens[2]['type'] == 'range', f"Unexpected label: {tokens[2]['val']}", tokens[2]['l_number'])
        tok_type = tokens[0]['val']
        ranges = [tokens[2]['val']]
        tokens = tokens[3:]
        while len(tokens) > 0:
            if tokens[0]['type'] == 'close_bracket':
                tokens = tokens[1:]
                break
            elif tokens[0]['type'] == 'comma':
                tokens = tokens[1:]
            elif tokens[0]['type'] == 'range':
                ranges.append(tokens[0]['val'])
            else:
                raise Exception(f"Unexpected token at line {tokens[0]['l_number']}: {tokens[0]['val']}")
        if tok_type == "except":
            for i in tokens:
                i_except.append(i)
        if tok_type == "exclude":
            for i in tokens:
                i_exclude.append(i)
        if tokens[0]['type'] == 'close_bracket':
            tokens = tokens[1:]
            break
        if tokens[0]['type'] == 'comma':
            tokens = tokens[1:]
    return {
        'i_name': i_name,
        'i_range': i_range,
        'except': [i for i in i_except],
        'exclude': [i for i in i_exclude]
    }, tokens
    


def parse_subgroup(tokens):
    sg_name = None
    sg_size = 0
    if tokens[0]['type'] == 'label':
        nadl_assert(tokens[0]['val'] not in ['inputs', 'outputs', 'group', 'groups'],
                    f"invalid group name: {tokens[0]['val']}", tokens[0]['l_number'])
        sg_name = tokens[0]['val']
        tokens = tokens[1:]
    if tokens[0]['type'] == 'int':
        sg_size = tokens[0]['val']
        tokens = tokens[1:]
    else:
        nadl_assert(False, f"invalid group definition: {tokens[0]['val']}\n\tCorrect definition looks like this: "
                            "\"<groupname> size x [...\", groupname is an optional label", tokens[0]['l_number'])
    # tokens = tokens[1:]
    nadl_assert(tokens[0]['type'] == 'by', f"invalid group definition: {tokens[0]['val']}\n\tCorrect definition looks like this: "
                                            "\"<groupname> size x [...\", groupname is an optional label", tokens[0]['l_number'])
    tokens = tokens[2:]
    depth = 1
    inputs = []
    c_input = {
        'ig_name': None,
        'range': None,
        'except': [],
        'exclude': []
    }
    # inputs[12:24] except[2] exclude[5:7] exclude[idx],
    while len(tokens) > 0:
        i_group, tokens = parse_group_input(tokens)
        if i_group is None:
            break
        inputs.append(i_group)
        if tokens[0]['type'] == 'close_bracket':
            tokens = tokens[1:]
            break
    return {
        "name": sg_name,
        "size": sg_size,
        "inputs": [i for i in inputs]
    }, tokens



def parse_group(tokens):
    print(f"Parsing {tokens}")
    g_name = tokens[0]['val']
    tokens = tokens[1:]
    g_items = []
    if (tokens[0]['type'] != 'colon') or (tokens[1]['type'] != 'open_bracket'):
        raise Exception(f"Syntax error at line {tokens[0]['l_number']}: Correct syntax is as following: \"groups: [...\" or \"outputs: [...\"")
    tokens = tokens[2:]
    counter = 0
    while len(tokens) > 0:
        if tokens[0]['type'] == 'comma':
            tokens = tokens[1:]
        elif tokens[0]['type'] == 'close_bracket':
            tokens = tokens[1:]
            break
        elif tokens[0]['type'] in ['int', 'label']:
            group, tokens = parse_subgroup(tokens)
            if group is None:
                break
            g_items.append(group)
        counter += 1
        if counter == 1000:
            raise Exception("We are stuck!")
    return g_items, g_name, tokens


# def parse_module(tokens):
#     mod_name, tokens = get_module_name(tokens)
#     mod_inputs = []
#     mod_groups = []
#     mod_outputs = []
#     counter = 0
#     while True:
#         cluster, cl_type, tokens = parse_cluster(tokens)
#         if cluster is None:
#             break
#         if cl_type == 'inputs':
#             for i in cluster:
#                 mod_inputs.append(i)
#         elif cl_type == 'groups':
#             for i in cluster:
#                 mod_groups.append(i)
#         elif cl_type == 'outputs':
#             for i in cluster:
#                 mod_outputs.append(i)
#         counter += 1
#         if counter == 1000:
#             raise Exception("We are stuck!")


def parse_module(tokens):
    mod_name = None
    mod_tokens = []
    nadl_assert(tokens[0]['val'] in ['module', 'inputs', 'groups', 'outputs'], f"Invalid token: {tokens[0]['val']}", tokens[0]['l_number'])
    if tokens[0]['val'] == 'module':
        nadl_assert(tokens[1]['type'] == 'colon', f"Invalid token: expected \":\", got: {tokens[1]['val']}", tokens[1]['l_number'])
        nadl_assert(tokens[2]['type'] == 'label', f"Invalid token: expected <module_name>, got: {tokens[2]['val']}", tokens[2]['l_number'])
        mod_name = tokens[2]['val']
        tokens = tokens[3:]
    else:
        mod_name = "default"
    while len(tokens) > 0:
        if tokens[0]['val'] == 'module':
            break
        mod_tokens.append(tokens[0])
        tokens = tokens[1:]
    return {
        'name': mod_name,
        'tokens': mod_tokens
    }, tokens


def new_parse_group(tokens):
    nadl_assert(tokens[0]['val'] in ['inputs', 'groups', 'outputs'], f"Invalid token: {tokens[0]['val']}", tokens[0]['l_number'])
    nadl_assert(tokens[1]['type'] == 'colon', f"Invalid token: expected \":\", got: {tokens[1]['val']}", tokens[1]['l_number'])
    nadl_assert(tokens[2]['type'] == 'open_bracket', f"Invalid token: expected \"[\"], got: {tokens[2]['val']}", tokens[2]['l_number'])
    depth = 1
    g_name = tokens[0]['val']
    g_tokens = []
    tokens = tokens[3:]
    while depth > 0:
        if len(tokens) == 0:
            raise Exception(f"Error: Unmatched brackets!")
        if tokens[0]['type'] == 'open_bracket':
            depth += 1
        elif tokens[0]['type'] == 'close_bracket':
            depth -= 1
        g_tokens.append(tokens[0])
        tokens = tokens[1:]
    return {
        'name': g_name,
        'tokens': g_tokens
    }, tokens


def parse_inputs_group(tokens):
    ranges = []
    while len(tokens) > 0:
        g_name = 'undefined'
        if tokens[0]['type'] == 'label':
            g_name = tokens[0]['val']
            tokens = tokens[1:]
        if tokens[0]['type'] == 'range':
            ranges.append({
                'name': g_name,
                'range': tokens[0]['val']
            })
            tokens = tokens[1:]
        if tokens[0]['type'] == 'comma':
            tokens = tokens[1:]
        elif tokens[0]['type'] == 'close_bracket':
            tokens = tokens[1:]
            break
        else:
            raise Exception(f"Error at line {tokens[0]['l_number']}: Unexpected token: {tokens[0]['val']}")
    return ranges, tokens


def new_parse_subgroup(tokens):
    print(f"Parsing {[t['val'] for t in tokens]}")
    sg_name = 'default'
    if tokens[0]['type'] == 'label':
        sg_name = tokens[0]['val']
        tokens = tokens[1:]
    nadl_assert(tokens[0]['type'] == 'int', f"Invalid syntax: expected an integer, got: {tokens[0]['val']}", tokens[0]['l_number'])
    nadl_assert(tokens[1]['type'] == 'by', f"Invalid syntax: expected \"x\", got: {tokens[1]['val']}", tokens[1]['l_number'])
    sg_size = tokens[0]['val']
    sg_tokens = []
    tokens = tokens[2:]
    nadl_assert(tokens[0]['type'] == 'open_bracket', f"Invalid syntax: expected \"[\", got: {tokens[0]['val']}", tokens[0]['l_number'])
    tokens = tokens[1:]
    depth = 1
    while len(tokens) > 0:
        print(tokens[0]['val'])
        if tokens[0]['type'] == 'open_bracket':
            depth += 1
        elif tokens[0]['type'] == 'close_bracket':
            depth -= 1
        if (tokens[0]['type'] == 'comma') and (depth == 0):
            tokens = tokens[1:]
            break
        sg_tokens.append(tokens[0])
        tokens = tokens[1:]
    # print([t['val'] for t in sg_tokens])
    return {
        'name': sg_name,
        'size': sg_size,
        'tokens': sg_tokens
    }, tokens

    


def parse_complex_range(tokens):
    nadl_assert(tokens[0]['type'] == 'open_bracket', f"Invalid syntax: expected \"[\", got: {tokens[0]['val']}", tokens[0]['l_number'])
    ranges = []
    tokens = tokens[1:]
    while len(tokens) > 0:
        if tokens[0]['type'] == 'comma':
            pass
        elif tokens[0]['type'] == 'range':
            ranges.append(tokens[0]['val'])
        elif tokens[0]['type'] == 'close_bracket':
            tokens = tokens[1:]
            break
        else:
            raise Exception(f"Error at line {tokens[0]['l_number']}: Unexpected token: {tokens[0]['val']}")
        tokens = tokens[1:]
    return ranges, tokens


def new_parse_group_inputs(tokens):
    # print(tokens[0])
    # i_source = None
    # i_ranges = []
    i_exclude = []
    i_except = []
    nadl_assert(tokens[0]['type'] == 'label', f"Invalid syntax: expected a group name, got: {tokens[0]['val']}", tokens[0]['l_number'])
    i_source = tokens[0]['val']
    tokens = tokens[1:]
    i_ranges, tokens = parse_complex_range(tokens)
    while len(tokens) > 0:
        if tokens[0]['type'] == 'close_bracket':
            tokens = tokens[1:]
            break
        elif tokens[0]['type'] == 'keyword':
            if tokens[0]['val'] not in ['except', 'exclude']:
                raise Exception(f"Error at line {tokens[0]['l_number']}: Unexpected token: {tokens[0]['val']}")
            if tokens[0]['val'] == 'except':
                ranges, tokens = parse_complex_range(tokens)
                for r in ranges:
                    i_except.append(r)
            elif tokens[0]['val'] == 'exclude':
                ranges, tokens = parse_complex_range(tokens)
                for r in ranges:
                    i_exclude.append(r)
    return {
        'source': i_source,
        'ranges': i_ranges,
        'exclude': i_exclude,
        'except': i_except
    }, tokens



# def main(filename):
#     with open(filename) as f:
#         data = f.read().split('\n')
#     lines = prepare_data(data)
#     for line in lines:
#         print(f"{line['l_number']}: {line['text']} [{line['len']}]")
#     # print("Tokens:\n\n\n")
#     tokens = update_ranges(tokenize(lines))
#     # for t in tokens:
#     #     print(t['val'])
#     modules = []
#     while len(tokens) > 0:
#         module, tokens = parse_module(tokens)
#         if module is None:
#             break
#         modules.append(module)
#     for i in range(len(modules)):
#         modules[i]['groups'] = []
#         tokens = modules[i]['tokens']
#         while len(tokens) > 0:
#             group, tokens = new_parse_group(tokens)
#             if group is None:
#                 break
#             modules[i]['groups'].append(group)
#     for i in range(len(modules)):
#         for j in range(len(modules[i]['groups'])):
#             tokens = modules[i]['groups'][j]['tokens']
#             g_type = modules[i]['groups'][j]['name']
#             group, tokens = new_parse_cluster(tokens, g_type)
#             # print(dir(group))
#             if g_type in ['groups', 'outputs']:
#                 for k in range(len(group['subgroups'])):
#                     group['subgroups'][k]['group_inputs'] = []
#                     tokens = group['subgroups'][k]['tokens']
#                     while len(tokens) > 0:
#                         g_input, tokens = new_parse_group_inputs(tokens)
#                         print(tokens, "\n")
#                         if g_input is not None:
#                             group['subgroups'][k]['group_inputs'].append(g_input)
#             modules[i]['groups'][j]['groups'] = group
#     with open('parse_result.json', 'w') as f:
#         f.write(json.dumps(modules, indent=4))
#     # for mod in modules:
#     #     print(f"Module name: {mod['name']}")
#     #     for group in mod['groups']:
#     #         print(f"Group name: {group['name']}")


def get_module_name(tokens):
    if tokens[0]['val'] == 'module':
        nadl_assert(tokens[1]['type'] == 'colon', f"Invalid token: expected \":\", got: {tokens[1]['val']}", tokens[1]['l_number'])
        nadl_assert(tokens[2]['type'] == 'label', f"Invalid token: expected <module_name>, got: {tokens[2]['val']}", tokens[2]['l_number'])
        mod_name = tokens[2]['val']
        tokens = tokens[3:]
    else:
        mod_name = "default"
    return mod_name, tokens


def parse_cluster(tokens):
    if tokens[0]['val']  == 'inputs':
        return parse_inputs(tokens[1:])
    elif tokens[0]['val'] in ['outputs', 'groups']:
        return parse_group(tokens)
    elif tokens[0]['val']  == 'module':
        return None, None, tokens
    else:
        raise Exception(f"Syntax error at line {tokens[0]['l_number']}: Invalid group name: \"{tokens[0]['val']}\"")


# def parse_cluster(tokens, g_type):
#     if g_type == 'inputs':
#         print('parsing inputs')
#         ranges, tokens = parse_inputs_group(tokens)
#         return {
#             'name': 'inputs',
#             'ranges': ranges
#         }, tokens
#     else:
#         print(f"parsing {g_type}")
#         subgroups = []
#         while len(tokens) > 0:
#             subgroup, tokens = new_parse_subgroup(tokens)
#             subgroups.append(subgroup)
#         return {
#             'name': g_type,
#             'subgroups': subgroups
#         }, tokens


def parse_module_inputs(tokens):
    """ Returns the ranges array [range0, range1, ...] and remaining tokens"""
    ranges = []
    while len(tokens) > 0:
        # print(tokens) 
        g_name = 'undefined'
        if tokens[0]['type'] == 'label':
            g_name = tokens[0]['val']
            tokens = tokens[1:]
        if tokens[0]['type'] == 'range':
            ranges.append({
                'name': g_name,
                'range': tokens[0]['val']
            })
            tokens = tokens[1:]
        if len(tokens) == 0:
            break
        if tokens[0]['type'] == 'comma':
            tokens = tokens[1:]
        elif tokens[0]['type'] == 'close_bracket':
            tokens = tokens[1:]
            break
        else:
            raise Exception(f"Error at line {tokens[0]['l_number']}: Unexpected token: {tokens[0]['val']}")
    return ranges


def parse_subgroups(tokens):
    ''' Returns [{'name': group name, 'size': int, 'tokens': [tokens]}, ...] '''
    subgroups = []
    while len(tokens) > 0:
        sg_name = 'undefined'
        if tokens[0]['type'] == 'label':
            sg_name = tokens[0]['val']
            tokens = tokens[1:]
        if tokens[0]['type'] == 'int':
            sg_size = tokens[0]['val']
            tokens = tokens[1:]
        nadl_assert(tokens[0]['type'] == 'by', f"Invalid token: expected: \"x\", got: {tokens[0]['val']}", tokens[0]['l_number'])
        nadl_assert(tokens[1]['type'] == 'open_bracket', f"Invalid token: expected: \"[\", got: {tokens[1]['val']}", tokens[1]['l_number'])
        tokens = tokens[2:]
        sg_tokens = []
        depth = 1
        while len(tokens) > 0:
            if tokens[0]['type'] == 'open_bracket':
                depth += 1
            elif tokens[0]['type'] == 'close_bracket':
                depth -= 1
            elif (tokens[0]['type'] == 'comma') and (depth == 0):
                tokens = tokens[1:]
                break
            sg_tokens.append(tokens[0])
            tokens = tokens[1:]
        subgroups.append({
            'name': sg_name,
            'size': sg_size,
            'tokens': sg_tokens
        })
    return subgroups


def check_module_group_definition(tokens):
    nadl_assert(tokens[0]['val'] in ['inputs', 'outputs', 'groups'],
                f"Invalid token: expected: \"inputs\"/\"groups\"/\"outputs\", got: {tokens[0]['val']}",
                tokens[0]['l_number'])
    nadl_assert(tokens[1]['type'] == 'colon', f"Invalid token: expected: \":\", got: {tokens[1]['val']}", tokens[1]['l_number'])
    nadl_assert(tokens[2]['type'] == 'open_bracket', f"Invalid token: expected: \"[\", got: {tokens[2]['val']}", tokens[2]['l_number'])


def get_module_group_tokens(tokens):
    g_name = tokens[0]['val']
    g_tokens = []
    tokens = tokens[3:]
    depth = 1
    while len(tokens) > 0:
        if tokens[0]['type'] == 'open_bracket':
            depth += 1
        elif tokens[0]['type'] == 'close_bracket':
            depth -= 1
        if depth == 0:
            tokens = tokens[1:]
            break
        g_tokens.append(tokens[0])
        tokens = tokens[1:]
    return g_name, g_tokens, tokens


def parse_module_groups(mod_name, tokens):
    """ A module group looks like this: inputs/groups/outputs: [...] """
    mod_groups = {}
    while len(tokens) > 0:
        check_module_group_definition(tokens)
        g_name, g_tokens, tokens = get_module_group_tokens(tokens)
        if g_name in mod_groups:
            raise Exception(f"Error: module {mod_name} contains multiple definitions of the {g_name} field")
        if g_name == 'inputs':
            i_ranges = parse_module_inputs(g_tokens)
            mod_groups['inputs'] = i_ranges
        elif g_name in ['groups', 'outputs']:
            s_groups = parse_subgroups(g_tokens)    # Returns [{'name': group name, 'size': int, 'tokens': [tokens]}, ...]
            # TODO: Add subgroup inputs parsing
            mod_groups[g_name] = s_groups
    return mod_groups


def parse_module_tokens(tokens):
    """ Returns {'name': module_name, 'tokens': [tokens]} """
    mod_name = None
    mod_tokens = []
    nadl_assert(tokens[0]['val'] in ['module', 'inputs', 'groups', 'outputs'], f"Invalid token: {tokens[0]['val']}", tokens[0]['l_number'])
    mod_name, tokens = get_module_name(tokens)
    while len(tokens) > 0:
        if tokens[0]['val'] == 'module':
            break
        mod_tokens.append(tokens[0])
        tokens = tokens[1:]
    return {
        'name': mod_name,
        'tokens': mod_tokens
    }, tokens


def check_module(mod_name, mod_groups):
    if 'inputs' not in mod_groups:
        raise Exception(f"Error: module {mod_name} does not contain definition of the \"inputs\" field!")
    if 'outputs' not in mod_groups:
        raise Exception(f"Error: module {mod_name} does not contain definition of the \"outputs\" field!")


def parse_modules(tokens):
    modules = {}
    while len(tokens) > 0:
        module, tokens = parse_module_tokens(tokens)        # Returns {'name': module_name, 'tokens': [tokens]} and tokens
        mod_groups = parse_module_groups(module['name'], module['tokens'])  # Returns {'inputs': [...], 'outputs': [...], 'groups': [...]}, groups may be missing
        modules[module['name']] = mod_groups
        check_module(module['name'], mod_groups)
    return modules


def new_main(filename):
    with open(filename) as f:
        data = f.read().split('\n')
    lines = prepare_data(data)
    for line in lines:
        print(f"{line['l_number']}: {line['text']} [{line['len']}]")
    # print("Tokens:\n\n\n")
    tokens = update_ranges(tokenize(lines))
    modules = parse_modules(tokens)
    with open('parse_result.json', 'w') as f:
        f.write(json.dumps(modules, indent=4))



if __name__ == "__main__":
    new_main("nadl_example.nad")
