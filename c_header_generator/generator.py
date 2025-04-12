import sys
import os
import argparse
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

class DefaultAwareAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)
        setattr(namespace, f'_{self.dest}_set_by_user', True)

# python generator.py --source filename --output-dir path
if __name__ == "__main__":
    
    n_types = {
        'linear': 0,
        'poly': 1
    }

    script_location = os.path.dirname(os.path.realpath(__file__))
    examples_folder = f"{script_location}/examples"
    default_source_file = f"{examples_folder}/simple_example.nad"

    parser = argparse.ArgumentParser(description='Optional app description')

    parser.add_argument('--source', nargs='?', default=f"{examples_folder}/simple_example.nad",
                        help='Source file', action=DefaultAwareAction)
    parser.add_argument('--output-dir', nargs='?', default=examples_folder,
                        help='Output directory', action=DefaultAwareAction)
    args = parser.parse_args()

    input_file = args.source
    output_dir = args.output_dir

    # If user specified the input file but hasn't specified the output directory, output to the same directory
    if hasattr(args, '_source_set_by_user') and not hasattr(args, '_output_dir_set_by_user'):
        output_dir = os.path.dirname(os.path.realpath(input_file))
        
    print(f"Processing file {input_file}")
    print(f"Output directory: {output_dir}")
    # sys.exit(0)
    modules = parse_file(input_file)
    with open(f"{output_dir}/parsing_results.json", 'w') as f:
        f.write(stringify_modules(modules))

    for module in modules:
        output_file =  f"{output_dir}/config_{module['name']}.h"
        mod_header = generate_neurons(module, n_types)
        for line in generate_structure(module):
            mod_header.append(line)
        with open(output_file, 'w') as f:
            f.write('\n'.join(mod_header))