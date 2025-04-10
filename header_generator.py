import sys
from nadl_parser import parse_file
from nadl_stringify import stringify_modules


# def get_exceptions_list(arr, self_idx, reverse=False):
#     exceptions = []
#     for e in arr:
#         if isinstance(e, list):
#             for idx in range(*e):
#                 exceptions.append(idx)
#         elif isinstance(e, int):
#             exceptions.append(e)
#         elif isinstance(e, str) and e == 'idx':
#             exceptions.append(self_idx)
#         else:
#             raise Exception("Error: invalid exceptions list")
#     exceptions = list(set(exceptions))
#     # print(f"{exceptions = }")
#     exceptions.sort(reverse=reverse)
#     return exceptions


# def add_to_header(config, header_lines):
#     temp_line = f"\t   {config['idx']},\t{config['num_inputs']},\t\t\t{config['type']},\t"
#     for i in config['indices']:
#         temp_line += f" {i},"
#     header_lines.append(temp_line)


# def find_group(module, group_name):
#     if group_name in ['inputs', 'groups', 'outputs']:
#         return module[group_name], module[group_name]['offset']
#     for group in module['inputs']['ranges']:
#         if group['name'] == group_name:
#             return module['inputs'][group_name], 0
#     for cluster in ['groups', 'outputs']:
#         for group in module[cluster]['ranges']:
#             if group['name'] == group_name:
#                 return module[cluster][group_name], module[cluster]['offset']
#     raise Exception(f"Error: undefined group name: {group_name}")


# def process_cluster(module, cluster_name, neuron_types, header_lines):
#     group_idx = 0
#     mod_name = module['name']
#     for group in module[cluster_name]['groups']:
#         for i in range(*group['range']):
#             idx = module[cluster_name]['offset'] + i
#             n_type = group['type']
#             inputs = []
#             for i_group in group['inputs']:
#                 # At least one of [idx, range] must be set
#                 i_temp = []
#                 g_name = i_group['name']
#                 g_arr, g_offset = find_group(module, g_name)
#                 excepts = get_exceptions_list(i_group['except'], i)
#                 excludes = get_exceptions_list(i_group['exclude'], i, reverse=True)
#                 if i_group['idx'] is None and len(i_group['range']) > 0:
#                     for temp_idx in range(*i_group['range']):
#                         if temp_idx not in excepts:
#                             i_temp.append(module[i_group['name']]['offset'] + temp_idx)
#                 elif i_group['idx'] is not None and len(i_group['range']) == 0:
#                     if g_name == 'inputs':
#                         arr = g_arr['ranges'][i_group['idx']]
#                     else:
#                         arr = g_arr['groups'][i_group['idx']]
#                     for temp_idx in range(g_offset+arr['range'][0], g_offset+g_arr['range'][1]):
#                         if temp_idx not in excepts:
#                             i_temp.append(module[i_group['name']]['offset'] + temp_idx)
#                 elif i_group['idx'] is not None and len(i_group['range']) > 0:
#                     pass
#                 else:
#                     raise Exception(f"Error: invalid config of the {mod_name}.groups.{group['name']}")
#                 for exclude_idx in excludes:
#                     if len(i_temp) > exclude_idx:
#                         i_temp.pop(exclude_idx)
#                 for add_idx in i_temp:
#                     inputs.append(add_idx)
#             if len(inputs) == 0:
#                 raise Exception(f"Error: {mod_name}.groups[{group_idx}]: "
#                                 f"\n\tNeuron {i} doesn't have inputs")
#             add_to_header({
#                 'idx': idx,
#                 'type': neuron_types[n_type],
#                 'num_inputs': len(inputs),
#                 'indices': inputs
#             }, header_lines)
#         group_idx += 1


# def generate_header(module, neuron_types):
#     mod_name = module['name']
#     # print(mod_name)
#     num_inputs = module['inputs']['size']
#     num_outputs = module['outputs']['size']
#     num_neurons = 0
#     module['inputs']['offset'] = 0
#     module['inputs']['range'] = [0, num_inputs]
#     offset = num_inputs
#     mod_group_size = 0
#     if 'groups' in module:
#         module['groups']['offset'] = num_inputs
#         module['groups']['range'] = [offset, offset + module['groups']['size']]
#         num_neurons += module['groups']['size']
#         offset += module['groups']['size']
#     module['outputs']['range'] = [offset, offset + module['outputs']['size']]
#     num_neurons += module['outputs']['size']
#     module['outputs']['offset'] = num_inputs + mod_group_size
#     header_lines = [
#         "#include <stdint.h>\n",
#         f"uint32_t {mod_name}_neurons[] = " + "{",
#         "    // idx  num_inputs  type indices"
#     ]
#     process_cluster(module, "groups", neuron_types, header_lines)
#     # process_cluster(module, "outputs", neuron_types, header_lines)
#     header_lines.append("};")
#     return header_lines

"""
uint32_t neurons[] = {
    // idx  num_inputs  type indices
       4,   4,          1,   0, 1, 2, 3,
       5,   4,          1,   0, 1, 2, 3,
       6,   4,          1,   0, 1, 2, 3,
       7,   4,          1,   0, 1, 2, 3,
       8,   4,          1,   4, 5, 6, 7,
};

micronet_map_t micronet_map = {
    .num_inputs = 4,
    .num_neurons = 5,
    .net_size = 9,
    .neurons = neurons,
    .num_outputs = 1,
    .output_indices = {8},
};
"""

def get_source_group(module, input_group_name):
    # raise Exception("ImplementMe!")
    return ''


def process_groups(module, mod_name, n_types, header):
    for group in module[mod_name]['groups']:
        header.append(f"\t\t// {mod_name}.{group['name']}:")
        offset = group['offset']
        n_type = group['type']
        for i in range(group['size']):
            idx = offset + i
            indices = []
            for i_group in group['inputs']:
                source_group = get_source_group(module, i_group['name'])
                if i_group['idx'] is None:
                    pass
                else:
                    pass


def generate_neurons(module, n_types):
    header = [
        "#include <stdint.h>\n",
        f"uint32_t {module['name']}_neurons[] = " + "{",
        "    // idx  num_inputs  type indices"
    ]
    num_inputs = module['inputs']['size']
    num_outputs = module['outputs']['size']
    num_neurons = 0
    if 'groups' in module:
        num_neurons += module['groups']['size']
        process_groups(module, 'groups', n_types, header)
    process_groups(module, 'outputs', n_types, header)
    num_neurons += module['outputs']['size']
    header.append("};\n")
    return header


def get_num_inputs(module):
    return module['inputs']['size']


def get_num_neurons(module):
    size = module['outputs']['size']
    if 'groups' in module:
        size += module['groups']['size']
    return size


def get_net_size(module):
    return get_num_inputs(module) + get_num_neurons(module)


def get_num_outputs(module):
    return module['outputs']['size']


def get_output_indices(module):
    indices = [f"{i}" for i in range(module['outputs']['range'][0], module['outputs']['range'][1])]
    return "{" + ", ".join(indices) + "}"


def generate_structure(module):
    return [
        "micronet_map_t micronet_map = {",
        f"\t.num_inputs = {get_num_inputs(module)},",
        f"\t.num_neurons = {get_num_neurons(module)},",
        f"\t.net_size = {get_net_size(module)},",
        f"\t.neurons = {module['name']}_neurons,",
        f"\t.num_outputs = {get_num_outputs(module)},",
        f"\t.output_indices = {get_output_indices(module)},",
        "};"
    ]


# def new_generate_header(module, n_types):
#     header = generate_neurons(module, n_types)
#     for line in generate_structure(module):
#         header.append(line)
#     return header


if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else "examples/nadl_example.nad"
    modules = parse_file(filename)
    
    n_types = {
        'linear': 0,
        'poly': 1
    }

    for module in modules:
        # mod_header = new_generate_header(module, n_types)
        mod_header = generate_neurons(module, n_types)
        for line in generate_structure(module):
            mod_header.append(line)
        with open(f"examples/config_{module['name']}.h", 'w') as f:
            f.write('\n'.join(mod_header))