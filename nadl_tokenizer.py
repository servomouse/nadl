symbols = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'g', 'k',
    'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
    'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G',
    'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
    'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '_'
]

digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

tokens = {
    ',': {'type': 'comma', 'val': ',', 'l_number': 0},
    'x': {'type': 'by', 'val': 'x', 'l_number': 0},
    ':': {'type': 'colon', 'val': ':', 'l_number': 0},
    '[': {'type': 'open_bracket', 'val': '[', 'l_number': 0},
    ']': {'type': 'close_bracket', 'val': ']', 'l_number': 0},
    'module': {'type': 'keyword', 'val': 'module', 'l_number': 0},
    'except': {'type': 'keyword', 'val': 'except', 'l_number': 0},
    'exclude': {'type': 'keyword', 'val': 'exclude', 'l_number': 0},
    'type': {'type': 'keyword', 'val': 'type', 'l_number': 0},
}


def pattern(elements, tokens):
    for i in range(len(elements)):
        if elements[i] is None:
            continue
        key, val = list(elements[i].items())[0]
        if tokens[i][key] != val:
            return False
    return True


def update_ranges(tokens):
    new_tokens = []
    i = 0
    group_idx_pattern = [{'type': 'label'}, {'type': 'open_bracket'}, None, {'type': 'close_bracket'}]
    while i < len(tokens):
        if tokens[i]['type'] == 'int':
            if pattern([ {'type': 'colon'}, {'type': 'int'}], tokens[i+1:]):
                new_tokens.append({
                    'type': 'range',
                    'val': [tokens[i]['val'], tokens[i+2]['val']],
                    'l_number': tokens[i]['l_number']
                })
                i += 2
            elif (tokens[i+1]['type'] == 'by') or pattern(group_idx_pattern, tokens[i-2:]):
                new_tokens.append({
                    'type': tokens[i]['type'],
                    'val': tokens[i]['val'],
                    'l_number': tokens[i]['l_number']
                })
            elif (tokens[i+1]['type'] == 'comma') or (tokens[i+1]['type'] == 'close_bracket'):
                new_tokens.append({
                    'type': 'range',
                    'val': [tokens[i]['val'], tokens[i]['val']+1],
                    'l_number': tokens[i]['l_number']
                })
            else:
                raise Exception(f"Error: unexpected token \"{tokens[i+1]['val']}\" at line {tokens[i+1]['l_number']}")
        else:
            new_tokens.append({
                'type': tokens[i]['type'],
                'val': tokens[i]['val'],
                'l_number': tokens[i]['l_number']
            })
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
    line = lines[0]['text']
    while len(line) > 0:
        t = starts_with_token(line, tokens)
        if t:
            line = line[len(tokens[t]['val']):].strip()
            lines[0]['text'] = line
            return {
                'type': tokens[t]['type'],
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
                return {
                    'type': 'label',
                    'val': tok,
                    'l_number': lines[0]['l_number']
                }, lines if len(line) > 0 else lines[1:]
            elif line[0] in digits:
                while len(line) > 0:
                    if line[0] in digits:
                        tok += line[0]
                        line = line[1:]
                    else:
                        break
                lines[0]['text'] = line
                return {
                    'type': 'int',
                    'val': int(tok),
                    'l_number': lines[0]['l_number']
                }, lines if len(line) > 0 else lines[1:]
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