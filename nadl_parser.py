import sys
from tokenizer import symbols, digits, tokenize


def prepare_data(data):
    config = []
    counter = 0
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


def get_inputs(tokens):
    # expected pattern: [<name> range, ...], name is optional
    pass


def get_module(tokens):
    mod_name, tokens = get_module_name(tokens)
    mod_layers, tokens = get_layers(tokens)
    print(f"Module name: {mod_name}")
    for layer in mod_layers:
        print(f"\tModule layer: {layer}")
        print(f"\tModule layer: {mod_layers[layer]}")
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
    for l in tokens:
        print(f"{l['token']}, ", end='')
    print('')
    modules = process_modules(tokens)


if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else "nadl_example.nad"
    parse(filename)
