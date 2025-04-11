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

def get_input_source(module, input_group_name):
    if input_group_name in ['inputs', 'groups', 'outputs']:
        return module[input_group_name]
    for group in module['inputs']['groups']:
        if group['name'] == input_group_name:
            return group
    if 'groups' in module:
        for group in module['groups']['groups']:
            if group['name'] == input_group_name:
                return group
    for group in module['outputs']['groups']:
        if group['name'] == input_group_name:
            return group
    raise Exception(f"Unknown group name: {input_group_name}")


def get_inputs(module, input_group, idx):
    input_indices = []
    inputs = get_input_source(module, input_group['name'])
    if input_group['idx'] is not None:
        inputs = inputs['groups'][input_group['idx']]
    if input_group['range'] == 'full':
        for i in range(inputs['size']):
            input_indices.append(inputs['offset']+i)
    else:
        for i in range(input_group['range'][0], input_group['range'][1]):
            input_indices.append(inputs['offset']+i)
    # Except list:
    except_list = []
    for r in input_group['except']:
        if isinstance(r, list):
            for i in range(r[0], r[1]):
                except_list.append(i)
        elif isinstance(r, str) and r == 'idx':
            except_list.append(idx)
    # Exclude list:
    exclude_list = []
    for r in input_group['exclude']:
        if isinstance(r, list):
            for i in range(r[0], r[1]):
                exclude_list.append(i)
        elif isinstance(r, str) and r == 'idx':
            exclude_list.append(idx)
    temp_arr = []
    for i in input_indices:
        if i not in except_list:
            temp_arr.append(i)
    fin_arr = []
    for i in range(len(temp_arr)):
        if i not in exclude_list:
            fin_arr.append(temp_arr[i])

    return fin_arr


def process_groups(module, mod_name, n_types, header):
    for group in module[mod_name]['groups']:
        header.append(f"\t// {mod_name}.{group['name']}:")
        offset = group['offset']
        n_type = group['type']
        for i in range(group['size']):
            idx = offset + i
            indices = []
            for i_group in group['inputs']:
                indices += get_inputs(module, i_group, i)
            ind_string = ', '.join([f'{j}' for j in indices])
            header.append(f"\t   {idx},\t{len(indices)},\t\t\t{n_types[group['type']]},\t\t{ind_string},")


def generate_neurons(module, n_types):
    header = [
        "#include <stdint.h>\n",
        f"uint32_t {module['name']}_neurons[] = " + "{",
        "    // idx  num_inputs  type \tindices"
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
