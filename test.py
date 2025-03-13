from new_tokenizer import tokenize
import re


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


def update_ranges(tokens):
    new_tokens = []
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if tokens[i]['type'] == 'int':
            if (tokens[i+1]['type'] == 'colon') and (tokens[i+2]['type'] == 'int'):
                val = f"{tokens[i]['val']}{tokens[i+1]['val']}{tokens[i+2]['val']}"
                t_len = tokens[i]['len'] + tokens[i+1]['len'] + tokens[i+2]['len']
                new_tokens.append({'type': 'range', 'len': t_len, 'val': [tokens[i]['val'], tokens[i+2]['val']], 'l_number': tokens[i]['l_number']})
                # print(f"{tok['l_number']}: range {val} [{t_len}]")
                i += 2
            elif (tokens[i+1]['type'] == 'comma') or (tokens[i+1]['type'] == 'close_bracket'):
                new_tokens.append({'type': 'range', 'len': tokens[i]['len'], 'val': [tokens[i]['val'], tokens[i]['val']], 'l_number': tokens[i]['l_number']})
                # print(f"{tok['l_number']}: range {tok['val']} [{tok['len']}]")
            elif tokens[i+1]['type'] == 'by':
                new_tokens.append({'type': tok['type'], 'len': tok['len'], 'val': tok['val'], 'l_number': tok['l_number']})
                # print(f"{tok['l_number']}: {tok['type']} {tok['val']} [{tok['len']}]")
            else:
                raise Exception(f"Error: unexpected token \"{tokens[i+1]['val']}\" at line {tokens[i+1]['l_number']}")
        else:
            new_tokens.append({'type': tok['type'], 'len': tok['len'], 'val': tok['val'], 'l_number': tok['l_number']})
            # print(f"{tok['l_number']}: {tok['type']} {tok['val']} [{tok['len']}]")
        i += 1
    return new_tokens


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


def parse_subgroup(tokens):
    sg_name = None
    sg_size = 0
    if tokens[0]['type'] == 'label':
        nadl_assert(tokens[0]['val'] in ['inputs', 'outputs'],
                    f"invalid group name: {tokens[0]['val']}", tokens[0]['l_number'])
        sg_name = tokens[0]['val']
        tokens = tokens[1:]
    if tokens[0]['type'] == 'int':
        sg_size = tokens[0]['val']
        tokens = tokens[1:]
    else:
        nadl_assert(False, f"invalid group definition: {tokens[0]['val']}\n\tCorrect definition looks like this: "
                            "\"<groupname> size x [...\", groupname is an optional label", tokens[0]['l_number'])
    tokens = tokens[1:]
    nadl_assert(tokens[0]['type'] == 'by', f"invalid group definition: {tokens[0]['val']}\n\tCorrect definition looks like this: "
                                            "\"<groupname> size x [...\", groupname is an optional label", tokens[0]['l_number'])
    tokens = tokens[2:]
    depth = 1
    inputs = []
    while depth > 0:
        if tokens[0]['type'] == 'label':
            i_name = tokens[0]['val']



def parse_group(tokens):
    g_name = tokens[0]['val']
    tokens = tokens[1:]
    g_items = []
    if (tokens[0]['type'] != 'colon') or (tokens[1]['type'] != 'open_bracket'):
        raise Exception(f"Syntax error at line {tokens[0]['l_number']}: Correct syntax is as following: \"groups: [...\" or \"outputs: [...\"")
    tokens = tokens[2:]
    while len(tokens) > 0:
        if tokens[0]['type'] == 'comma':
            tokens = tokens[1:]
        elif tokens[0]['type'] == 'close_bracket':
            break
        elif tokens[0]['type'] in ['int', 'label']:
            group, tokens = parse_subgroup(tokens)
            g_items.append(group)
    return g_items, g_name, tokens


def parse_cluster(tokens):
    if tokens[0]['val']  == 'inputs':
        return parse_inputs(tokens[1:])
    elif tokens[0]['val'] in ['outputs', 'groups']:
        return parse_group(tokens)
    elif tokens[0]['val']  == 'module':
        return None, None, tokens
    else:
        raise Exception(f"Syntax error at line {tokens[0]['l_number']}: Invalid group name: \"{tokens[0]['val']}\"")


def parse_module(tokens):
    mod_name, tokens = get_module_name(tokens)
    mod_inputs = []
    mod_groups = []
    mod_outputs = []
    while True:
        cluster, cl_type, tokens = parse_cluster(tokens)
        if cluster is None:
            break
        if cl_type == 'inputs':
            for i in cluster:
                mod_inputs.append(i)
        elif cl_type == 'groups':
            for i in cluster:
                mod_groups.append(i)
        elif cl_type == 'outputs':
            for i in cluster:
                mod_outputs.append(i)


def main(filename):
    with open(filename) as f:
        data = f.read().split('\n')
    lines = prepare_data(data)
    for line in lines:
        print(f"{line['l_number']}: {line['text']} [{line['len']}]")
    print("Tokens:\n\n\n")
    tokens = update_ranges(tokenize(lines))
    for t in tokens:
        print(t['val'])
    modules = []
    while True:
        module, tokens = parse_module(tokens)
        if module is None:
            break
        modules.append(module)
    print(modules)


if __name__ == "__main__":
    main("nadl_example.nad")
