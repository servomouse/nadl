#include <stdint.h>

uint32_t example_net_neurons[] = {
    // idx  num_inputs  type indices
		// groups.layer0:
		// groups.layer1:
		// groups.layer3:
		// groups.layer4:
		// outputs.undefined:
};

micronet_map_t micronet_map = {
	.num_inputs = 64,
	.num_neurons = 44,
	.net_size = 108,
	.neurons = example_net_neurons,
	.num_outputs = 4,
	.output_indices = {104, 105, 106, 107},
};