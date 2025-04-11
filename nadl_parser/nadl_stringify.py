
def stringify_inputs(module, indent, i_symbol, output):
    output.append(i_symbol*indent + f"\"inputs\": " + "{")
    indent += 1
    output.append(i_symbol*indent + f"\"size\": " + f"{module['inputs']['size']},")
    output.append(i_symbol*indent + f"\"offset\": " + f"{module['inputs']['offset']},")
    output.append(i_symbol*indent + f"\"range\": " + f"{module['inputs']['range']},")
    output.append(i_symbol*indent + f"\"groups\": " + "[")
    indent += 1
    for i_group in module['inputs']['groups']:
        output.append(i_symbol*indent + "{")
        indent += 1
        output.append(i_symbol*indent + f"\"name\": " + f"\"{i_group['name']}\",")
        output.append(i_symbol*indent + f"\"size\": " + f"{i_group['size']},")
        output.append(i_symbol*indent + f"\"offset\": " + f"{i_group['offset']},")
        output.append(i_symbol*indent + f"\"range\": " + f"{i_group['range']}")
        indent -= 1
        output.append(i_symbol*indent + "},")
    output[-1] = output[-1][:-1]    # Remove the last comma
    indent -= 1
    output.append(i_symbol*indent + "]")
    indent -= 1
    output.append(i_symbol*indent + "},")


def stringify_group(group, indent, i_symbol, output, g_name):
    output.append(i_symbol*indent + f"\"{g_name}\": " + "{")
    indent += 1
    output.append(i_symbol*indent + f"\"size\": " + f"{group['size']},")
    output.append(i_symbol*indent + f"\"offset\": " + f"{group['offset']},")
    output.append(i_symbol*indent + f"\"range\": " + f"{group['range']},")
    output.append(i_symbol*indent + f"\"groups\": " + "[")
    indent += 1
    for i_group in group['groups']:
        output.append(i_symbol*indent + "{")
        indent += 1
        output.append(i_symbol*indent + f"\"name\": " + f"\"{i_group['name']}\",")
        output.append(i_symbol*indent + f"\"size\": " + f"{i_group['size']},")
        output.append(i_symbol*indent + f"\"offset\": " + f"{i_group['offset']},")
        output.append(i_symbol*indent + f"\"range\": " + f"{i_group['range']},")
        output.append(i_symbol*indent + f"\"type\": " + f"\"{i_group['type']}\",")
        output.append(i_symbol*indent + "\"inputs\": [")
        indent += 1
        for g_input in i_group['inputs']:
            i_range = g_input['range']
            if i_range == 'full':
                i_range = "\"full\""
            output.append(i_symbol*indent + "{")
            indent += 1
            output.append(i_symbol*indent + f"\"name\": " + f"\"{g_input['name']}\",")
            if g_input['idx'] is None:
                output.append(i_symbol*indent + f"\"idx\": " + "null,")
            else:
                output.append(i_symbol*indent + f"\"idx\": " + f"{g_input['idx']},")
            output.append(i_symbol*indent + f"\"range\": " + f"{i_range},")
            output.append(i_symbol*indent + f"\"except\": " + f"{g_input['except']},".replace("'", "\""))
            output.append(i_symbol*indent + f"\"exclude\": " + f"{g_input['exclude']}".replace("'", "\""))
            indent -= 1
            output.append(i_symbol*indent + "},")
        output[-1] = output[-1][:-1]    # Remove the last comma
        indent -= 1
        # output.append(i_symbol*indent + f"\"inputs\": " + f"{i_group['inputs']},")
        output.append(i_symbol*indent + "]")
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
    indent += 1
    for module in modules:
        output.append(i_symbol * indent + "{")
        indent += 1
        output.append(i_symbol*indent + f"\"name\": \"{module['name']}\",")
        stringify_inputs(module, indent, i_symbol, output)  # Inputs
        if 'groups' in module:
            stringify_group(module['groups'], indent, i_symbol, output, 'groups')
        stringify_group(module['outputs'], indent, i_symbol, output, 'outputs')
        output[-1] = output[-1][:-1]    # Remove the last comma
        indent -= 1
        output.append(i_symbol * indent + "},")
    output[-1] = output[-1][:-1]    # Remove the last comma
    indent -= 1
    output.append("]")
    return "\n".join(output)