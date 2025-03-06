NADL (Network Architecture Description Language) is a simple language used for creating simple and effitient description of a neural network architecture.
The syntax is very simple:
    inputs syntax: [<name> range]
    groups and outputs syntax: [<name> size x [range <exclude[range]> <except[range]>] type]
        exclude takes a subarray from the original array excluding the given range of indices,
        except takes a subarray from a given array and then excludes the given range of indices.

    For example:
    inputs: [0:7]    -> 0, 1, 2, 3, 4, 5, 6, 7
    groups: [
        4 x [inputs[2:6 exclude[3]]]  # take inputs[2:6] excluding inputs[3]
        4 x [inputs[2:6 except[3]]]   # take inputs[2:6] end exclude result[3]
    ]

Example configuration:

module: micronet

    inputs: [
        0,      # single index
        1:32    # range
    ]

    groups: [
        8 x [inputs[0:16] except[idx]] type linear,
        8 x [inputs[16:31]] type linear,
        4 x [group[0], group[1]] type linear
    ]

    outputs: [
        4 x [group[2]] type poly
    ]

Such configuration will be unfolded into the following structure:

{
    "inputs": [
        {"name": None, "size": 1, "range": [0]},
        {"name": None, "size": 31, "range": [1, 32]}
    ],
    "groups": [
        {
            "name": None,
            "group_size": 8,
            "num_inputs": 16,
            "indices": [
                {"source": ["inputs"], "range": [0, 15], "except": ["idx"], "exclude": []},
            ],
            "type": "linear"
        },
        {
            "name": None,
            "group_size": 8,
            "num_inputs": 16,
            "indices": [
                {"source": ["inputs"], "range": [15, 31], "except": [], "exclude": []},
            ],
            "type": "linear"
        },
        {
            "name": None,
            "group_size": 4,
            "num_inputs": 32,
            "indices": [
                {"source": ["groups", 0], "range": ["full"], "except": [], "exclude": []},
                {"source": ["groups", 1], "range": ["full"], "except": [], "exclude": []},
            ],
            "type": "linear"
        },
    ],
    "outputs": [
        {
            "name": None,
            "group_size": 4,
            "num_inputs": 4,
            "indices": [
                {"source": ["groups", 2], "range": ["full], "except": [], "exclude": []},
            ],
            "type": "poly"
        },
    ]
}
