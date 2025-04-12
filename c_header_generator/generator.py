import sys
import os
from struct_generator import generate_structure
from array_generator import generate_neurons
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from nadl_parser import parse_file, stringify_modules


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


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "examples/nadl_example.nad"
    modules = parse_file(input_file)
    output_file = sys.argv[2] if len(sys.argv) > 2 else f"examples/config_{module['name']}.h"
    with open(f"parsing_results.json", 'w') as f:
        f.write(stringify_modules(modules))
    
    n_types = {
        'linear': 0,
        'poly': 1
    }

    for module in modules:
        mod_header = generate_neurons(module, n_types)
        for line in generate_structure(module):
            mod_header.append(line)
        with open(output_file, 'w') as f:
            f.write('\n'.join(mod_header))