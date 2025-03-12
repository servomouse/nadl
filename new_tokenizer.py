symbols = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'g', 'k',
    'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
    'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G',
    'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
    'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '_'
]

digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

tokens = {
    ',': {'type': 'comma', 'len': 1, 'text': ',', 'l_number': 0},
    ':': {'type': 'colon', 'len': 1, 'text': ':', 'l_number': 0},
    '[': {'type': 'open_bracket', 'len': 1, 'text': '[', 'l_number': 0},
    ']': {'type': 'close_bracket', 'len': 1, 'text': ']', 'l_number': 0},
    'except': {'type': 'keyword', 'len': 6, 'text': 'except', 'l_number': 0},
    'exclude': {'type': 'keyword', 'len': 7, 'text': 'exclude', 'l_number': 0},
    'type': {'type': 'keyword', 'len': 4, 'text': 'type', 'l_number': 0},
    'idx': {'type': 'keyword', 'len': 3, 'text': 'idx', 'l_number': 0},
}


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
                'text': tokens[t]['text'],
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
                return {'type': 'label', 'len': len(tok), 'text': tok, 'l_number': lines[0]['l_number']}, lines if len(line) > 0 else lines[1:]
            elif line[0] in digits:
                while len(line) > 0:
                    if line[0] in digits:
                        tok += line[0]
                        line = line[1:]
                    else:
                        break
                lines[0]['text'] = line
                return {'type': 'int', 'len': len(tok), 'text': int(tok), 'l_number': lines[0]['l_number']}, lines if len(line) > 0 else lines[1:]
    return None, lines[1:]


def tokenize(lines):
    tokens = []
    counter = 0
    while True:
        counter += 1
        token, lines = parse_token(lines)
        if ((token is None) and (len(lines) == 0)) or (counter == 100):
            break
        if token is not None:
            tokens.append(token)
    return tokens