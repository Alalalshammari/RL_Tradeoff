import math
def loops_number(rlConfig4):
    with open(rlConfig4) as f:
        reading_text = f.read()
        text_lines = reading_text.split('\n')
        loops_num = int(text_lines[0])
        return loops_num
def loops_structure(rlConfig4):
    loop_indexes = []
    loop_sequences = {}
    with open(rlConfig4) as f:
        lines = f.readlines()
        for line in lines[1:]:
            if ":" not in line:
                break
            index, sequence_str = line.split(":")
            index = int(index)
            sequence = [int(n) for n in sequence_str.strip()[1:-1].split(',')]
            loop_indexes.append(index)
            loop_sequences[index] = sequence
    return loop_indexes, loop_sequences
def read_nodes(loop_sequences):
    nodes_in_loops_seqs = [val for seq in loop_sequences.values() for val in seq]
    Nmin = min(nodes_in_loops_seqs)
    Nmax = max(nodes_in_loops_seqs)
    rlConfigSize = (Nmax+1)
    rlConfig = int(math.sqrt(rlConfigSize))
    return Nmin, Nmax, rlConfigSize, rlConfig
def Nodes_2D_Matrix(Nmin, rlConfig):
    matrix = [[None for _ in range(rlConfig)] for _ in range(rlConfig)]
    node = Nmin
    for i in range(rlConfig):
        for j in range(rlConfig):
            matrix[i][j] = node
            node += 1
    return matrix
def innerNodes_2D_Matrix(matrix, rlConfig):
    inner_matrices = []
    inner_config = rlConfig - 2
    while inner_config > 1:
        first_inner_node = (rlConfig - inner_config) // 2
        inner_matrix = [[None for _ in range(inner_config)] for _ in range(inner_config)]
        for i in range(inner_config):
            for j in range(inner_config):
                inner_matrix[i][j] = matrix[first_inner_node + i][first_inner_node + j]
        inner_matrices.append(inner_matrix)
        inner_config -= 2
    return inner_matrices
def loops_in_layers(loop_sequences, layer, inner_layer=True):
    Nmin = layer[0][0]
    Nmax = layer[-1][-1]
    common_loops = {}
    for loop_index, sequence in loop_sequences.items():
        if inner_layer:
            if Nmin in sequence and Nmax in sequence and set(sequence).issubset(set([layer_nodes for inner_set in layer for layer_nodes in inner_set])):
                common_loops[loop_index] = sequence
        else:
            if any(node in sequence for node in [layer_nodes for inner_set in layer for layer_nodes in inner_set]):
                common_loops[loop_index] = sequence
    return common_loops

rlConfig4 = "rlConfig4.txt"
loops_num = loops_number(rlConfig4)
print(f"loops number = {loops_num}")
loop_indexes, loop_sequences = loops_structure(rlConfig4)
print(f"Loop indexes: {loop_indexes}")
print("Loop sequences:")
for sequences in loop_sequences.values():
    print(sequences)
Nmin, Nmax, rlConfigSize, rlConfig = read_nodes(loop_sequences)
print(f"\nMin Node Index: {Nmin}")
print(f"Max Node Index: {Nmax}")
print(f"NxN Size: {rlConfigSize}")
print(f"NxN Configuration: {rlConfig}x{rlConfig}")
main_matrix = Nodes_2D_Matrix(Nmin, rlConfig)
print("\nMain Layer:")
for k in main_matrix:
    print(k)
inner_middle_matrices = innerNodes_2D_Matrix(main_matrix, rlConfig)
for inner_matrices_counter, matrix in enumerate(inner_middle_matrices, start=1):
    print(f"\nInner Layer {inner_matrices_counter} (Configuration {len(matrix)}x{len(matrix[0])}):")
    for t in matrix:
        print(t)
print("\nMain Layer Loops:")
loops_in_MainLayers = loops_in_layers(loop_sequences, main_matrix, inner_layer=False)
for loop_index, sequence in loops_in_MainLayers.items():
    print(f"Loop {loop_index}: {sequence}")
for inner_matrices_counter, matrix in enumerate(inner_middle_matrices, start=1):
    print(f"\nInner Layer {inner_matrices_counter} (Configuration {len(matrix)}x{len(matrix[0])}) Loops:")
    intersected_loops_inner = loops_in_layers(loop_sequences, matrix, inner_layer=True)
    for loop_index, sequence in intersected_loops_inner.items():
        print(f"Loop {loop_index}: {sequence}")
