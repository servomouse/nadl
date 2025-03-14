symbols = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'g', 'k',
    'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
    'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G',
    'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
    'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '_'
]

digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

tokens = {
    ',': {'type': 'comma', 'len': 1, 'val': ',', 'l_number': 0},
    'x': {'type': 'by', 'len': 1, 'val': 'x', 'l_number': 0},
    ':': {'type': 'colon', 'len': 1, 'val': ':', 'l_number': 0},
    '[': {'type': 'open_bracket', 'len': 1, 'val': '[', 'l_number': 0},
    ']': {'type': 'close_bracket', 'len': 1, 'val': ']', 'l_number': 0},
    'module': {'type': 'keyword', 'len': 6, 'val': 'module', 'l_number': 0},
    'except': {'type': 'keyword', 'len': 6, 'val': 'except', 'l_number': 0},
    'exclude': {'type': 'keyword', 'len': 7, 'val': 'exclude', 'l_number': 0},
    'type': {'type': 'keyword', 'len': 4, 'val': 'type', 'l_number': 0},
    # 'idx': {'type': 'range', 'len': 3, 'val': 'idx', 'l_number': 0},
}


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
        elif (tokens[i]['type'] == 'int') and (tokens[i+1]['type'] == 'close_bracket'):
                new_tokens.append({'type': 'range', 'len': t_len, 'val': 'idx', 'l_number': tokens[i]['l_number']})
                i += 1
        else:
            new_tokens.append({'type': tok['type'], 'len': tok['len'], 'val': tok['val'], 'l_number': tok['l_number']})
            # print(f"{tok['l_number']}: {tok['type']} {tok['val']} [{tok['len']}]")
        i += 1
    return new_tokens


def starts_with_token(line, tokens):
    for t in tokens:
        if line.startswith(t):
            return t
    return False


def parse_token(lines):
    global tokens
    if len(lines) == 0:
        return None, []
    # print(f"Parsing {lines[0]['text']}")
    line = lines[0]['text']
    while len(line) > 0:
        t = starts_with_token(line, tokens)
        if t:
            line = line[tokens[t]['len']:].strip()
            lines[0]['text'] = line
            return {
                'type': tokens[t]['type'],
                'len': tokens[t]['len'],
                'val': tokens[t]['val'],
                'l_number': lines[0]['l_number']
            }, lines if len(line) > 0 else lines[1:]
        elif line[0] == ' ':
            line = line[1:]
        else:
            tok = ''
            if line[0] in symbols:
                while len(line) > 0:
                    if (line[0] in symbols) or (line[0] in digits):
                        tok += line[0]
                        line = line[1:]
                    else:
                        break
                lines[0]['text'] = line
                return {'type': 'label', 'len': len(tok), 'val': tok, 'l_number': lines[0]['l_number']}, lines if len(line) > 0 else lines[1:]
            elif line[0] in digits:
                while len(line) > 0:
                    if line[0] in digits:
                        tok += line[0]
                        line = line[1:]
                    else:
                        break
                lines[0]['text'] = line
                return {'type': 'int', 'len': len(tok), 'val': int(tok), 'l_number': lines[0]['l_number']}, lines if len(line) > 0 else lines[1:]
    return None, lines[1:]


def tokenize(lines):
    tokens = []
    counter = 0
    while True:
        counter += 1
        token, lines = parse_token(lines)
        if ((token is None) and (len(lines) == 0)) or (counter == 1000):
            break
        if token is not None:
            tokens.append(token)
    return tokens