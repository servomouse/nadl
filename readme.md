
# NADL (Network Architecture Description Language)

## Introduction

NADL is a language used to describe the architecture of neural networks. It views a network   
as a set of groups, where each group represents a collection of neurons. This   
approach allows efficient description of complex network architectures   
even without clearly defined layers and backward connections.

## Syntax

### Inputs

The inputs section defines the input groups of the network. The syntax for inputs is as follows:

    <group name> <range>: a group of input nodes, where:  
        <group name> is an optional label for the group
        <range> is either a single integer (e.g., 0) or a range of integers (e.g., 1:32)

The division into groups is optional.

#### Examples:

    inputs: [
        main_input 0,           # single index
        secondary_input 1:8,    # range, named group
        8:32                    # range, unnamed group
    ]

In this example, the network has three input groups:   
- main_input containing a single input with an index 0  
- secondary_input containing inputs 1, 2, 3, 4, 5, 6 and 7 
- unnamed group with a range of indices from 8 to 31.

Another example:

    inputs: [
        0:64    # simple range without groups
    ]

If groups are present, inputs can be addressed as follows:

    inputs[0]           # addresses the entire group 0
    inputs[main_input]  # addresses the entire group named "main_input"
    inputs[0:32]        # addresses all the inputs
    inputs[1][4:8]      # addresses inputs 4, 5, 6 and 7 of the group 1

### Groups and Outputs

The groups and outputs sections define the hidden and output groups of the network,   
respectively. The syntax for groups and outputs is identical:

    <group name> <size> x [<ranges>] type <typename>: a group of neurons, where:
        <group name> is an optional label for the group
        <size> is the number of neurons in the group
        <ranges> is a description of the input connections for each   
            neuron in the group. The syntax is as following:   
            <source group>[<range>]
        <typename> is the type of the neurons in the group (e.g., linear,   
            poly). Type name is just a user defined label allowing creating   
            networks containing different types of neurons

The ``<ranges>`` syntax is as follows:

    inputs[:]: connects each neuron in the group to each input node

    inputs[<range>]: connects each neuron in the group to the input nodes   
        in the specified range

    inputs[<range>] except [<exclude range>]: connects each neuron in the   
        group to the input nodes in the specified range, excluding the   
        indices specified in <exclude range>

    inputs[<range>] exclude [<exclude range>]: connects each neuron in the   
        group to the input nodes in the specified range, excluding the   
        indices specified in <exclude range> from the resulting array

Note that ``<exclude range>`` can be a single index, a range of indices or even a list    
of them (e.g., [2], [3:7], [idx, 2:5]). This can result in some neurons in a group    
having a different number of inputs. For example:

    groupname 5 x [inputs[2:7] except[idx, 3]] type typename

This example will create the following 5 neurons:

    groupname[0]: inputs[2, 4, 5 and 6]  # indices 2 to 7 excluding 3 and 0    
                                           (but 0 is not present)
    groupname[1]: inputs[2, 4, 5 and 6]  # indices 2 to 7 excluding 3 and 1    
                                           (but 1 is not present)
    groupname[2]: inputs[4, 5 and 6]     # indices 2 to 7 excluding 3 and 2
    groupname[3]: inputs[2, 4, 5 and 6]  # indices 2 to 7 excluding 3 and 3
    groupname[4]: inputs[2, 5 and 6]     # indices 2 to 7 excluding 3 and 4

#### Examples:

    group_name 8 x [inputs[0:16] except [3:5]] type linear: connects each   
        neuron in the group to the input nodes in the range 0:16,   
        excluding indices 3, 4, and 5

    group_name 8 x [inputs[0:16] exclude [3:5]] type linear: connects each   
        neuron in the group to the input nodes in the range 0:16,   
        excluding indices 3, 4, and 5 from the resulting array

    group_name 8 x [inputs[0:16] except [idx]] type linear: connects each   
        neuron in the group to the input nodes in the range 0:16,   
        excluding the index of the neuron itself

### Full Example

Here is a full example of a NADL configuration:

    module: micronet

        inputs: [
            main_input 0,      # single index
            1:31    # range
        ]

        groups: [
            group_name 8 x [inputs[0:16] except [3:5]] type linear,
            4 x [group[0]] type poly
        ]

        outputs: [
            4 x [group[1]] type linear
        ]

This example defines a neural network with 32 inputs divided into two groups, two hidden groups of 8 and 4 neurons, and one output group containig 4 outputs.