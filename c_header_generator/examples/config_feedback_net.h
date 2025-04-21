#include <stdint.h>

uint32_t feedback_net_neurons[] = {
    // idx  num_inputs  type 	indices
	// groups.undefined:
	   8,	9,			1,		0, 1, 2, 3, 4, 5, 6, 7, 9,
	   9,	9,			1,		0, 1, 2, 3, 4, 5, 6, 7, 10,
	   10,	9,			1,		0, 1, 2, 3, 4, 5, 6, 7, 11,
	   11,	9,			1,		0, 1, 2, 3, 4, 5, 6, 7, 12,
	   12,	9,			1,		0, 1, 2, 3, 4, 5, 6, 7, 13,
	   13,	9,			1,		0, 1, 2, 3, 4, 5, 6, 7, 14,
	   14,	9,			1,		0, 1, 2, 3, 4, 5, 6, 7, 15,
	   15,	9,			1,		0, 1, 2, 3, 4, 5, 6, 7, 16,
	// groups.undefined:
	   16,	8,			1,		0, 1, 2, 3, 4, 5, 6, 7,
	// outputs.undefined:
	   17,	9,			1,		8, 9, 10, 11, 12, 13, 14, 15, 16,
};

micronet_map_t feedback_net_micronet_map = {
	.num_inputs = 8,
	.num_neurons = 10,
	.net_size = 18,
	.neurons = feedback_net_neurons,
	.num_outputs = 1,
	.output_indices = {17},
};