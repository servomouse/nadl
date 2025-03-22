import sys
import json
from nadl_parser import parse_file


def range_is_valid(g_start, g_end, g_name, groups):
    for g in groups:
        if (g_start >= g[0] and g_start < g[1]) or (g_end > g[0] and g_end < g[1]):
            raise Exception(f"Error: intersecting ranges: {g_name} and {g[2]}")
    return True


def module_get_inputs(module):
    # print(module)
    inputs = module['inputs']
    i_size = 0
    i_groups = []
    i_ranges = []
    for g in inputs:
        g_name = g['name']
        g_start = g['range'][0]
        g_end = g['range'][1]
        g_size = g_end - g_start if g_end > g_start else 1
        i_size += g_size
        if range_is_valid(g_start, g_end, g_name, i_groups):
            i_groups.append([g_start, g_end, g_name])
            i_ranges.append({'name': g_name, 'range': [g_start, g_end]})
    return {
        'size': i_size,
        'ranges': i_ranges
    }


def module_get_groups(groups):
    cluster = {
        'size': 0,
        'groups': []
    }
    for group in groups:
        g_range = [cluster['size'], cluster['size'] + group['size']]
        cluster['size'] += group['size']
        cluster['groups'].append({
            'name': group['name'],
            'size': group['size'],
            'range': g_range,
            'type': group['type'],
            'inputs': group['inputs']
        })
    return cluster


def stringify_inputs(module, indent, i_symbol, output):
    output.append(i_symbol*indent + f"\"inputs\": " + "{")
    indent += 1
    output.append(i_symbol*indent + f"\"size\": " + f"{module['inputs']['size']},")
    output.append(i_symbol*indent + f"\"ranges\": " + "[")
    indent += 1
    for i_group in module['inputs']['ranges']:
        output.append(i_symbol*indent + "{")
        indent += 1
        output.append(i_symbol*indent + f"\"name\": " + f"{i_group['name']},")
        output.append(i_symbol*indent + f"\"range\": " + f"{i_group['range']},")
        indent -= 1
        output.append(i_symbol*indent + "},")
    output[-1] = output[-1][:-1]    # Remove the last comma
    indent -= 1
    output.append(i_symbol*indent + "]")
    indent -= 1
    output.append(i_symbol*indent + "},")


def stringify_modules(modules, use_tabs:bool = True):
    output = []
    indent = 0
    i_symbol = "\t" if use_tabs else "    "
    output.append("[\n")
    for module in modules:
        indent = 1
        output.append(i_symbol * indent + "{\n")
        indent = 2
        output.append(i_symbol*indent + f"\"name\": \"{module['name']}\",")
        
        stringify_inputs(module, indent, i_symbol, output)  # Inputs
        # Groups:
        if 'groups' in module:
            output.append(i_symbol*indent + f"\"groups\": " + "{")
            for i_group in module['groups']:
                pass
            output.append(i_symbol*indent + "},")
        # Outputs:
        output.append(i_symbol*indent + f"\"outputs\": " + "{")
        for i_group in module['outputs']:
            pass
        output.append(i_symbol*indent + "},")
        output.append(i_symbol * indent + "}\n")
    output.append("]\n")
    for line in output:
        print(line)


def get_header(filename):
    modules = parse_file(filename)
    new_modules = []
    for m_name in modules:
        # inputs = module['inputs']
        # new_inputs = module_get_inputs(modules[m_name])
        # print(new_inputs)
        # new_groups = None
        # if 'groups' in modules[m_name]:
        #     new_groups = module_get_groups(modules[m_name]['groups'])
        # print(new_groups)
        # new_groups = []
        # outputs = module['outputs']
        new_modules.append({
            "name": m_name,
            'inputs': module_get_inputs(modules[m_name]),
            'groups': module_get_groups(modules[m_name]['groups']) if 'groups' in modules[m_name] else None,
            'outputs': module_get_groups(modules[m_name]['outputs'])
        })
    
    with open('parse_result_new.json', 'w') as f:
        f.write(json.dumps(new_modules, indent=4))
    stringify_modules(new_modules, False)


if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else "nadl_example.nad"
    get_header(filename)