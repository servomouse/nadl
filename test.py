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

a = r"\w+ \d+ x \[((?:\w+\[\d+\](?:, )?|\w+\[\d+:\d+\](?:, )?)*)\]\s*type\s*\w+"

group_description_regex = r"groups\s*:\s*\[\s*(\w+\s*\d+\s*x\s*\[(\b(?!except|exclude)\w+\b\s*\[\d+(?::\d+)?\](?:\s+(except|exclude)\s*\[\d+(?::\d+)?\])*(?:,\s*)?)+\]\s+type\s+\w+\s*(,\s*)?)+\s*\]"

a = r"\w*\s*\d+\s*x\s*\[(\b(?!except|exclude)\w+\b\s*\[\d+(?::\d+)?\](?:\s+(except|exclude)\s*\[\d+(?::\d+)?\])*(?:,\s*)?)+\]\s+type\s+\w+\s*((,\s*)|\])"

i_range = "\w*\s*\d+(?::\d+){0,1}\s*"
r_inputs = f"inputs\s*:\s*\[\s*({i_range},\s*)*\s*{i_range}\]"

group_name = "\b(?!except|exclude)\w+\b"
g_range = "\[\d+(?::\d+)?\]"
g_inputs = f"(\s*{group_name}\s*{g_range}(?:\s+(except|exclude)\s*{g_range})*"
g_definition = f"(\w*\s*\d+\s*x\s*\[{g_inputs},)*{g_inputs})+\s*\]\s+type\s+\w+\s*"
r_groups = f"groups\s*:\s*\[\s*{g_definition},\s*)*{g_definition})+\s*\]"

# r_groups = f"groups\s*:\s*\[\s*(\w*\s*\d+\s*x\s*\[(\s*\b(?!except|exclude)\w+\b\s*\[\d+(?::\d+)?\](?:\s+(except|exclude)\s*\[\d+(?::\d+)?\])*,)*(\s*\b(?!except|exclude)\w+\b\s*\[\d+(?::\d+)?\](?:\s+(except|exclude)\s*\[\d+(?::\d+)?\])*)+\s*\]\s+type\s+\w+\s*,\s*)*(\w*\s*\d+\s*x\s*\[(\s*\b(?!except|exclude)\w+\b\s*\[\d+(?::\d+)?\](?:\s+(except|exclude)\s*\[\d+(?::\d+)?\])*,)*(\s*\b(?!except|exclude)\w+\b\s*\[\d+(?::\d+)?\](?:\s+(except|exclude)\s*\[\d+(?::\d+)?\])*)+\s*\]\s+type\s+\w+\s*)+\s*\]"

r_outputs = f"outputs\s*:\s*\[\s*{g_definition},\s*)*{g_definition})+\s*\]"

# r_module = r"module\s*:\s*\w+\s*((inputs\s*:\s*\[\s*(\w*\s*\d+(?::\d+){0,1}\s*,\s*)*\s*\w*\s*\d+(?::\d+){0,1}\s*\])|(groups\s*:\s*\[\s*(\w*\s*\d+\s*x\s*\[(\b(?!except|exclude)\w+\b\s*\[\d+(?::\d+)?\](?:\s+(except|exclude)\s*\[\d+(?::\d+)?\])*(?:,\s*)?)+\]\s+type\s+\w+\s*(,\s*)?)+\s*\])|(outputs\s*:\s*\[\s*(\w*\s*\d+\s*x\s*\[(\b(?!except|exclude)\w+\b\s*\[\d+(?::\d+)?\](?:\s+(except|exclude)\s*\[\d+(?::\d+)?\])*(?:,\s*)?)+\]\s+type\s+\w+\s*(,\s*)?)+\s*\]))+"

# r_mod_new = r"(?=.*(inputs\s*:\s*\[\s*(\w*\s*\d+(?::\d+){0,1}\s*,\s*)*\s*\w*\s*\d+(?::\d+){0,1}\s*\])))(?=.*(outputs\s*:\s*\[\s*(\w*\s*\d+\s*x\s*\[(\b(?!except|exclude)\w+\b\s*\[\d+(?::\d+)?\](?:\s+(except|exclude)\s*\[\d+(?::\d+)?\])*(?:,\s*)?)+\]\s+type\s+\w+\s*(,\s*)?)+\s*\]))[(inputs\s*:\s*\[\s*(\w*\s*\d+(?::\d+){0,1}\s*,\s*)*\s*\w*\s*\d+(?::\d+){0,1}\s*\]))(outputs\s*:\s*\[\s*(\w*\s*\d+\s*x\s*\[(\b(?!except|exclude)\w+\b\s*\[\d+(?::\d+)?\](?:\s+(except|exclude)\s*\[\d+(?::\d+)?\])*(?:,\s*)?)+\]\s+type\s+\w+\s*(,\s*)?)+\s*\]))(groups\s*:\s*\[\s*(\w*\s*\d+\s*x\s*\[(\b(?!except|exclude)\w+\b\s*\[\d+(?::\d+)?\](?:\s+(except|exclude)\s*\[\d+(?::\d+)?\])*(?:,\s*)?)+\]\s+type\s+\w+\s*(,\s*)?)+\s*\])]+"

a = r_inputs
b = r_groups
c = r_outputs
r_module = f"{r_module}?(?=[{a}{c}{b}]*{a})(?=[{a}{c}{b}]*{c})[{a}{c}{b}]+"

def prepare_data(data):
    clean_data = []
    counter = 1
    for d in data:
        temp = d.split('#')[0].strip()
        if len(temp) > 0:
            clean_data.append(f"*** {counter} *** " + temp)
        counter += 1
    return ' '.join(clean_data)


def main(filename):
    with open(filename) as f:
        data = f.read().split('\n')
    data = prepare_data(data)
    print(data)
    print(replace_substring(data, "\*\*\* \d* \*\*\*", ''))
    # if 'module' in data:
    #     data = data.split('module')
    # else:
    #     raise Exception("Error: Specify at least one module like this:\n"
    #                     "module: modulename\n"
    #                     "\tinputs: [inputs config>]\n"
    #                     "\tgroups: [groups config>]\n"
    #                     "\toutputs: [outputs config>]\n")
    # for i in data:
    #     print(i)
    # print(extract_substring(data, 'inputs:'))
    # print(extract_substring(data, 'groups:'))
    # print(extract_substring(data, 'outputs:'))


if __name__ == "__main__":
    main("nadl_example.nad")
