

symbols = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'g', 'k',
    'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
    'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G',
    'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
    'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '_'
]

digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


def checkx(string, line):
    if (string[0] == 'x') and (string[1] in [' ', '[', '\n']):
        return
    raise Exception(f"Unexpected symbol after 'x' at line {line['line_number']}: {line['data']}\n"
                    "\tCorrect syntax looks like this: <size> x [...")


def parse_range(string, line):
    values = ['']
    current_idx = 0
    while len(string) > 0:
        if string[0] in digits:
            values[current_idx] += string[0]
            string = string[1:]
        elif string[0] == ':':
            if current_idx == 0:
                current_idx = 1
                values.append('')
                string = string[1:]
            else:
                raise Exception(f"Incorrect syntax at line {line['line_number']}: {line['data']}, [{string}]\n"
                                "\tCorrect syntax looks like this: 123 or 5:123")
        elif string[0] in [',', ']', '[']:
            return values, string
        elif string[0] == ' ':
            if current_idx == 1 and len(values[1] > 0):
                return values, string[1:]
            string = string[1:]
        else:
            break
            # raise Exception(f"Incorrect syntax at line {line['line_number']}: {line['data']}, [{string}]\n"
            #                 "\tCorrect syntax looks like this: 123 or 5:123")
    return values, string


def get_label_type(token):
    keywords = ['module', 'inputs', 'groups', 'outputs', 'except', 'exclude', 'type']
    if token in keywords:
        return 'keyword'
    if token == 'idx':
        return 'own_index'
    return 'label'


def parse_label(string):
    # print(f"Parsing label in {string}")
    label = ''
    while len(string) > 0:
        if (string[0] in symbols) or (string[0] in digits):
            label += string[0]
            string = string[1:]
        else:
            break
    return label, string


def tokenize(data):
    tokens = [] # [{'token': "lalala', 'token_type': 'str', 'line_number': 123"} ...]
    current_token = ''
    tokens_dict = {
        ',': 'comma',
        ':': 'colon',
        '[': 'open_bracket',
        ']': 'close_bracket',
    }
    for line in data:
        string = line['data']
        # print(f"Parsing string {line['line_number']}: {string}")
        while len(string) > 0:
            if string[0] in tokens_dict:
                tokens.append({
                    'token': string[0],
                    'token_type': tokens_dict[string[0]],
                    'line_number': line['line_number']
                })
                string = string[1:]
            elif string[0] == 'x':
                checkx(string, line)
                tokens.append({'token': 'x', 'token_type': 'by', 'line_number': line['line_number']})
                string = string[1:]
            # elif string[0] == ' ':
            #     string = string[1:]
            elif string[0] in digits:
                t, string = parse_range(string, line)
                tokens.append({'token': t, 'token_type': 'range', 'line_number': line['line_number']})
            elif string[0] in symbols:
                label, string = parse_label(string)
                n_type = get_label_type(label)
                tokens.append({'token': label, 'token_type': n_type, 'line_number': line['line_number']})
            else:
                string = string[1:]
    return tokens
