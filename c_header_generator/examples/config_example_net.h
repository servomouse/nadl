#include <stdint.h>

uint32_t example_net_neurons[] = {
    // idx  num_inputs  type 	indices
	// groups.layer0:
	   24,	19,			0,		0, 1, 2, 3, 4, 5, 6, 8, 9, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
	   25,	19,			0,		0, 1, 2, 3, 4, 5, 6, 8, 9, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
	   26,	19,			0,		0, 1, 2, 3, 4, 5, 6, 8, 9, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
	   27,	19,			0,		0, 1, 2, 3, 4, 5, 6, 8, 9, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
	   28,	19,			0,		0, 1, 2, 3, 4, 5, 6, 8, 9, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
	   29,	19,			0,		0, 1, 2, 3, 4, 5, 6, 8, 9, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
	   30,	19,			0,		0, 1, 2, 3, 4, 5, 6, 8, 9, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
	   31,	19,			0,		0, 1, 2, 3, 4, 5, 6, 8, 9, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
	// groups.layer1:
	   32,	3,			0,		5, 6, 7,
	   33,	3,			0,		4, 6, 7,
	   34,	3,			0,		4, 5, 7,
	   35,	3,			0,		4, 5, 6,
	   36,	4,			0,		4, 5, 6, 7,
	   37,	4,			0,		4, 5, 6, 7,
	   38,	4,			0,		4, 5, 6, 7,
	   39,	4,			0,		4, 5, 6, 7,
	// groups.layer2:
	   40,	4,			0,		8, 9, 10, 11,
	   41,	4,			0,		8, 9, 10, 11,
	   42,	4,			0,		8, 9, 10, 11,
	   43,	4,			0,		8, 9, 10, 11,
	   44,	4,			0,		8, 9, 10, 11,
	   45,	4,			0,		8, 9, 10, 11,
	   46,	4,			0,		8, 9, 10, 11,
	   47,	4,			0,		8, 9, 10, 11,
	// groups.layer3:
	   48,	16,			0,		24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
	   49,	16,			0,		24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
	   50,	16,			0,		24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
	   51,	16,			0,		24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
	   52,	16,			0,		24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
	   53,	16,			0,		24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
	   54,	16,			0,		24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
	   55,	16,			0,		24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
	   56,	16,			0,		24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
	   57,	16,			0,		24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
	   58,	16,			0,		24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
	   59,	16,			0,		24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
	   60,	16,			0,		24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
	   61,	16,			0,		24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
	   62,	16,			0,		24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
	   63,	16,			0,		24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
	// groups.layer4:
	   64,	8,			0,		40, 41, 42, 43, 44, 45, 46, 47,
	   65,	8,			0,		40, 41, 42, 43, 44, 45, 46, 47,
	   66,	8,			0,		40, 41, 42, 43, 44, 45, 46, 47,
	   67,	8,			0,		40, 41, 42, 43, 44, 45, 46, 47,
	   68,	8,			0,		40, 41, 42, 43, 44, 45, 46, 47,
	   69,	8,			0,		40, 41, 42, 43, 44, 45, 46, 47,
	   70,	8,			0,		40, 41, 42, 43, 44, 45, 46, 47,
	   71,	8,			0,		40, 41, 42, 43, 44, 45, 46, 47,
	// outputs.undefined:
	   72,	8,			1,		64, 65, 66, 67, 68, 69, 70, 71,
	   73,	8,			1,		64, 65, 66, 67, 68, 69, 70, 71,
	   74,	8,			1,		64, 65, 66, 67, 68, 69, 70, 71,
	   75,	8,			1,		64, 65, 66, 67, 68, 69, 70, 71,
};

micronet_map_t example_net_micronet_map = {
	.num_inputs = 24,
	.num_neurons = 52,
	.net_size = 76,
	.neurons = example_net_neurons,
	.num_outputs = 4,
	.output_indices = {72, 73, 74, 75},
};