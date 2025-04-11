"""
Generates array like this:
uint32_t neurons[] = {
    // idx  num_inputs  type indices
       4,   4,          1,   0, 1, 2, 3,
       5,   4,          1,   0, 1, 2, 3,
       6,   4,          1,   0, 1, 2, 3,
       7,   4,          1,   0, 1, 2, 3,
       8,   4,          1,   4, 5, 6, 7,
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
