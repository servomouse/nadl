from new_tokenizer import tokenize, update_ranges
import json
import sys


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


def parse_module_inputs(tokens):
    """ Returns the ranges array [range0, range1, ...] and remaining tokens"""
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


def parse_complex_range(tokens):
    nadl_assert(tokens[0]['type'] == 'open_bracket', f"Invalid syntax: expected \"[\", got: {tokens[0]['val']}", tokens[0]['l_number'])
    ranges = []
    tokens = tokens[1:]
    while len(tokens) > 0:
        if tokens[0]['type'] == 'comma':
            pass
        elif tokens[0]['type'] == 'range':
            ranges.append(tokens[0]['val'])
        elif tokens[0]['type'] == 'label' and tokens[0]['val'] == 'idx':
            ranges.append(tokens[0]['val'])
        elif tokens[0]['type'] == 'close_bracket':
            tokens = tokens[1:]
            break
        else:
            raise Exception(f"Error at line {tokens[0]['l_number']}: Unexpected token: {tokens[0]['val']} of type {tokens[0]['type']}")
        tokens = tokens[1:]
    return ranges, tokens


def parse_subgroup_inputs_and_type(tokens):
    while len(tokens) > 0:
        nadl_assert(tokens[0]['type'] == 'label', f"Expected a label, got: {tokens[0]['val']}", tokens[0]['l_number'])
        nadl_assert(tokens[1]['type'] == 'open_bracket', f"Expected \"[\", got: {tokens[1]['val']}", tokens[1]['l_number'])
        s_name = tokens[0]['val']
        source_ranges, tokens = parse_complex_range(tokens[1:])
        s_range = [i for i in source_ranges]
        s_except = []
        s_exclude = []
        while len(tokens) > 0:
            if tokens[0]['type'] == 'close_bracket':
                tokens = tokens[1:]
                break
            elif tokens[0]['type'] == 'keyword':
                nadl_assert(tokens[1]['type'] == 'open_bracket', f"Expected: \"[\", got: {tokens[1]['val']}", tokens[1]['l_number'])
                if tokens[0]['val'] == 'except':
                    temp_ranges, tokens = parse_complex_range(tokens[1:])
                    for t in temp_ranges:
                        s_except.append(t)
                elif tokens[0]['val'] == 'exclude':
                    temp_ranges, tokens = parse_complex_range(tokens[1:])
                    for t in temp_ranges:
                        s_exclude.append(t)
                else:
                    raise Exception(f"Error at line {tokens[0]['l_number']}: Unexpected token: {tokens[0]['val']}")
            else:
                raise Exception(f"Error at line {tokens[0]['l_number']}: Unexpected token: {tokens[0]['val']}")
        nadl_assert(tokens[0]['type'] == 'keyword', f"Expected \"type\", got: {tokens[0]['val']}", tokens[0]['l_number'])
        nadl_assert(tokens[0]['val'] == 'type', f"Expected \"type\", got: {tokens[0]['val']}", tokens[0]['l_number'])
        nadl_assert(tokens[1]['type'] == 'label', f"Expected a label, got: {tokens[1]['val']}", tokens[1]['l_number'])
        s_type = tokens[1]['val']
        return {
            's_name': s_name,
            's_range': s_range,
            's_exclude': s_exclude,
            's_except': s_except,
            'sg_type': s_type
        }


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
            mod_groups[g_name] = {}
            mod_groups[g_name]['groups'] = []
            s_groups = parse_subgroups(g_tokens)    # Returns [{'name': group name, 'size': int, 'tokens': [tokens]}, ...]
            for sg in s_groups:
                temp = parse_subgroup_inputs_and_type(sg['tokens'])
                mod_groups[g_name]['groups'].append({
                    'name': sg['name'],
                    'size': sg['size'],
                    's_name': temp['s_name'],
                    's_range': temp['s_range'],
                    's_exclude': temp['s_exclude'],
                    's_except': temp['s_except'],
                    'sg_type': temp['sg_type']
                })
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


def parse_file(filename):
    with open(filename) as f:
        data = f.read().split('\n')
    lines = prepare_data(data)
    for line in lines:
        print(f"{line['l_number']}: {line['text']} [{line['len']}]")
    tokens = update_ranges(tokenize(lines))
    modules = parse_modules(tokens)
    with open('parse_result.json', 'w') as f:
        f.write(json.dumps(modules, indent=4))


if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else "nadl_example.nad"
    parse_file(filename)
