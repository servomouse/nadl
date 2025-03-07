import sys
from tokenizer import symbols, digits, tokenize


def prepare_data(data):
    config = []
    counter = 1
    for l in data.split("\n"):
        temp = l.strip()
        if temp.startswith("#") or len(temp) == 0:
            counter += 1
            continue
        elif '#' in temp:
            temp = temp.split("#")[0].strip()
        config.append({"line_number": counter, "data": temp})
        counter += 1
    return config


def get_module_name(tokens):
    if tokens[0]['token'] == 'module':
        if tokens[1]['token_type'] != 'colon':
            raise Exception(f"Invalid syntax at line {tokens[1]['line_number']}: "
                            f"expected syntax: module: modulename, got: module{tokens[1]['token']}{tokens[2]['token']}")
        if tokens[2]['token_type'] != 'label':
            raise Exception(f"Invalid syntax at line {tokens[2]['line_number']}: "
                            f"expected: modulename, got: {tokens[2]['token']}")
        return tokens[2]['token'], tokens[3:]
    if tokens[0]['token'] in ['inputs', 'groups', 'outputs']:
        return 'default', tokens
    else:
        raise Exception(f"Invalid syntax at line {tokens[0]['line_number']}: "
                        f"expected: \"module\" or \"inputs\" or \"groups\" or \"outputs\", got: {tokens[0]['token']}")


def prepare_layer(tokens):
    depth = 1
    layer_tokens = []
    while depth > 0:
        if tokens[0]['token_type'] == 'close_bracket':
            depth -= 1
        elif tokens[0]['token_type'] == 'open_bracket':
            depth += 1
        layer_tokens.append(tokens[0])
        tokens = tokens[1:]
    return layer_tokens, tokens


def get_layers(tokens):
    if tokens[0]['token'] not in ['inputs', 'groups', 'outputs']:
        raise Exception(f"Invalid syntax at line {tokens[0]['line_number']}: "
                        f"expected: \"module\" or \"inputs\" or \"groups\" or \"outputs\", got: {tokens[0]['token']}")
    if (tokens[1]['token_type'] != 'colon') or (tokens[2]['token_type'] != 'open_bracket'):
        raise Exception(f"Invalid syntax at line {tokens[1]['line_number']}: "
                        f"expected syntax: {tokens[0]['token']}: [..., "
                        f"got: {tokens[0]['token']}{tokens[1]['token']}{tokens[2]['token']}")
    layers = {}
    while len(tokens) > 0:
        if tokens[0]['token'] not in ['inputs', 'groups', 'outputs']:
            break
        layer_name = tokens[0]['token']
        layer_tokens, tokens = prepare_layer(tokens[3:])
        if not layer_name in layers:
            layers[layer_name] = layer_tokens
    return layers, tokens


# def get_irange(tokens):
#     s_range = ['']
#     tok_idx = 0
#     if tokens[0]['token_type'] == 'range':
#         s_range[0] += tokens[0]['token']
#     if tokens[1]['token_type'] == 'colon':
#         if tokens[2]['token_type'] == 'range':
#             s_range.append(tokens[2]['token'])
#             tok_idx = 3
#         else:
#             raise Exception(f"Error at line {tokens[2]['line_number']}: expected: range, got: {tokens[2]['token']}")
#     elif (tokens[1]['token_type'] == 'comma') or (tokens[1]['token_type'] == 'close_bracket'):
#         tok_idx = 2
#     else:
#         raise Exception(f"Error at line {tokens[1]['line_number']}: expected: "
#                         f"\",\", \':\' or \"]\", got: {tokens[1]['token']}")
#     i_range = []
#     r_size = 1
#     for i in range(len(s_range)):
#         i_range.append(int(s_range[i]))
#     if len(i_range) == 2:
#         if i_range[0] >= i_range[1]:
#             raise Exception(f"Error: invalid range at line {tokens[0]['line_number']}: "
#                             f"{tokens[0]['token']}{tokens[1]['token']} {tokens[2]['token']}")
#         r_size = i_range[1] - i_range[0] + 1
#     tokens = tokens[tok_idx:]
#     return r_size, i_range, tokens


def get_input_range_size(token):
    r_size = 1
    r_range = [int(token['token'][0])]
    if len(token['token']) == 2:
        r_range.append(int(token['token'][1]))
        if r_range[0] >= r_range[1]:
            raise Exception(f"Error: invalid range at line {token['line_number']}: "
                            f"The second value must be larger than the first; got: {r_range[0]}: {r_range[1]}")
        else:
            r_size = r_range[1] - r_range[0]
    return r_size


def get_inputs(tokens):
    # expected pattern: [<name> range, ...], name is optional
    inputs = []
    if tokens[0]['token_type'] == 'open_bracket':
        tokens = tokens[1:]
    while len(tokens) > 0:
        if tokens[0]['token_type'] == 'range':
            # r_size, i_range, tokens = get_irange(tokens)
            inputs.append({
                "label": None,
                "size": get_input_range_size(tokens[0]),
                "range": tokens[0]['token']
            })
            tokens = tokens[1:]
        elif tokens[0]['token_type'] == 'label':
            if tokens[1]['token_type'] == 'range':
                label = tokens[0]['token']
                # r_size, i_range, tokens = get_irange(tokens)
                inputs.append({
                    "label": label,
                    "size": get_input_range_size(tokens[1]),
                    "range": tokens[1]['token']
                })
                tokens = tokens[2:]
            else:
                raise Exception(f"Error: unexpected token at line {tokens[1]['line_number']}. "
                                f"Expected: range, got: {tokens[1]['token']}")
        elif tokens[0]['token_type'] == 'comma':
            tokens = tokens[1:]
        elif (tokens[0]['token_type'] == 'close_bracket') and (len(tokens) == 1):
            break
        else:
            raise Exception(f"Error: unexpected token at line {tokens[0]['line_number']}. "
                            f"Expected: group name or range, got: {tokens[0]['token']}")
    return inputs


def get_list_of_ranges(tokens):
    r_list = []
    while len(tokens) > 0:
        if (tokens[0]['token_type'] == 'range') or (tokens[0]['token_type'] == 'own_index'):
            r_list.append(tokens[0]['token'])
            tokens = tokens[1:]
        elif (tokens[0]['token_type'] == 'open_bracket') and \
                (tokens[1]['token_type'] == 'range') and \
                (tokens[2]['token_type'] == 'close_bracket'):
            r_list.append(tokens[1]['token'])
            tokens = tokens[3:]
        elif tokens[0]['token_type'] == 'comma':
            tokens = tokens[1:]
        elif tokens[0]['token_type'] == 'close_bracket':
            tokens = tokens[1:]
            break
        else:
            raise Exception(f"Invalid syntax at line {tokens[0]['line number']}: the correct syntax is \"except[<range>...")
    return r_list, tokens


def get_input_range(tokens):
    # print(f"\tParsing: {tokens[:5]}")
    r_label = None
    r_indices = []
    r_exclude = []
    r_except = []

    if tokens[0]['token_type'] == 'close_bracket':
        return None, tokens[1:]

    if (tokens[0]['token_type'] == 'label') or (tokens[0]['token_type'] == 'keyword'):
        r_label = tokens[0]['token']
        tokens = tokens[1:]
    else:
        raise Exception(f"Error at line {tokens[0]['line_number']}: input range should start from a label, not from {tokens[0]['token']}")

    if (tokens[0]['token_type'] != "open_bracket") or (tokens[1]['token_type'] != "range") or (tokens[2]['token_type'] != "close_bracket"):
        raise Exception(f"Invalid syntax at line {tokens[0]['line_number']}: "
                        f"Expected: \"{r_label}: [<range>]\", got: {r_label} {tokens[0]['token']} {tokens[1]['token']} {tokens[2]['token']}")
    r_indices = tokens[1]['token']
    tokens = tokens[3:]
    while len(tokens) > 0:
        if tokens[0]['token'] == 'except':
            if tokens[1]['token_type'] != 'open_bracket':
                raise Exception(f"Invalid syntax at line {token[1]['line_number']}: the correct syntax is \"except[<range>...")
            tokens = tokens[2:]
            r_list, tokens = get_list_of_ranges(tokens)
            r_except += r_list
        elif tokens[0]['token'] == 'exclude':
            if tokens[1]['token_type'] != 'open_bracket':
                raise Exception(f"Invalid syntax at line {tokens[1]['line_number']}: the correct syntax is \"exclude[<range>...")
            tokens = tokens[2:]
            r_list, tokens = get_list_of_ranges(tokens)
            r_exclude += r_list
        elif tokens[0]['token_type'] == 'comma':
            tokens = tokens[1:]
        else:
            break
    return {
                "name": r_label,
                "indices": r_indices,
                "except": r_except,
                "exclude": r_exclude
            }, tokens
            

def get_subgroup(tokens):
    # print(f"\tParsing: {tokens[:5]}")
    g_name = None
    g_size = 0
    g_indices = []
    g_type = None

    if tokens[0]['token_type'] == 'close_bracket':
        return None, tokens[1:]
    
    if tokens[0]['token_type'] not in ['label', 'range', 'keyword']:
        raise Exception(f"Invalid syntax it line{tokens[0]['line_number']}: subgroup definition should "
                        f"start from a label, a keyword or a range; got: {tokens[0]['token']}")

    if (tokens[0]['token_type'] == 'label') or (tokens[0]['token_type'] == 'keyword'):
        g_name = tokens[0]['token']
        tokens = tokens[1:]
    if tokens[0]['token_type'] == 'range':
        if len(tokens[0]['token']) > 1:
            raise Exception(f"Error at line {tokens[0]['line_number']}: Set group size using a single integer, not \"int: int\"")
        g_size = tokens[0]['token']
        tokens = tokens[1:]
    if (tokens[0]['token_type'] != 'by') or (tokens[1]['token_type'] != 'open_bracket'):
        raise Exception(f"Invalid sintax at line {tokens[0]['line_number']}: "
                        f"Expected syntax: \"<group_name> <range> x [...\", got {tokens[0]['token']} {tokens[1]['token']}")
    tokens = tokens[2:]
    while len(tokens) > 0:
        r, tokens = get_input_range(tokens)
        if r is None:
            break
        g_indices.append(r)
    if tokens[0]['token_type'] == 'comma':
        tokens = tokens[1:]
    if (tokens[0]['token_type'] == 'keyword') and (tokens[0]['token'] == 'type') and (tokens[1]['token_type'] == 'label'):
        g_type = tokens[1]['token']
        tokens = tokens[2:]
    if tokens[0]['token_type'] == 'comma':
        tokens = tokens[1:]
    return {
        "name": g_name,
        "group_size": g_size,
        "indices": g_indices,
        "type": g_type
    }, tokens



def get_group(tokens):
    group = []
    while len(tokens) > 0:
        subgroup, tokens = get_subgroup(tokens)
        if subgroup is None:
            break
        group.append(subgroup)
    return group


def get_module(tokens):
    mod_name, tokens = get_module_name(tokens)
    mod_layers, tokens = get_layers(tokens)
    mod_inputs = get_inputs(mod_layers['inputs'])
    mod_groups = get_group(mod_layers['groups'])
    mod_outputs = get_group(mod_layers['outputs'])
    print(f"Module name: {mod_name}")
    print(f"Module inputs: {mod_inputs}")
    print("Module groups:")
    for i in range(len(mod_groups)):
        print(f"\t{mod_groups[i]}")
    print("Module outputs:")
    for i in range(len(mod_outputs)):
        print(f"\t{mod_outputs[i]}")
    # for layer in mod_layers:
    #     print(f"\tModule layer: {layer}")
    #     print(f"\tModule layer: {mod_layers[layer]}")
    print(f"Remaining tokens: {tokens}")
    return mod_name, None, None


def process_modules(tokens):
    modules = {}
    while True:
        module_name, module, tokens = get_module(tokens)
        if module is None:
            break
        if not module_name in modules:
            modules[module_name] = module
        else:
            raise Exception(f"Error: two modules with the same name ({module_name})!")
    return modules


# def group_tokens(tokens):
#     groups = {}
#     while len(tokens) > 0:
#         if token[0]['token'] == 'module' and \
#            token[1]['token_type'] == 'colon' and \
#            token[2]['token_type'] == 'label':
#             if token[2]['token'] in groups:
#                 raise Exception(f"Error: two modules with the same name ({module_name})!")
#             groups[token[2]['token']] = {}


def parse(filename):
    with open(filename) as f:
        data = f.read()
    # config = parse_item(data)
    data = prepare_data(data)
    tokens = tokenize(data)
    # for l in tokens:
    #     print(f"{l['token']}, ", end='')
    # print('')
    modules = process_modules(tokens)


if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else "nadl_example.nad"
    parse(filename)
