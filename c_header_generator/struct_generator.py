"""
generates a network description structure like this:
micronet_map_t micronet_map = {
    .num_inputs = 4,
    .num_neurons = 5,
    .net_size = 9,
    .neurons = neurons,
    .num_outputs = 1,
    .output_indices = {8},
};
"""

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
