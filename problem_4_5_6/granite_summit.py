from qiskit import QuantumCircuit
import bluequbit

# Step 1: Load full circuit
qc = QuantumCircuit.from_qasm_file("/Users/shaiverma/Documents/Quantum/YQuantum2025/Shai/P5_granite_summit.qasm")

# Step 2: Define 20 CZs to cut
czs_to_cut = [
    (2, 8), (2, 8), (8, 20), (8, 20), (17, 21), (17, 21),
    (10, 26), (10, 26), (5, 31), (5, 31), (30, 32), (30, 32),
    (0, 32), (0, 32), (4, 33), (4, 33), (25, 34), (25, 34),
    (15, 25), (15, 25)
]

# Step 3: Remove selected CZs
def remove_selected_czs(circuit, cz_pairs):
    new_circ = QuantumCircuit(circuit.num_qubits, circuit.num_clbits)

    # Create a mapping from original qubits to new circuit qubits
    qubit_map = {q: new_circ.qubits[i] for i, q in enumerate(circuit.qubits)}

    for instr, qargs, cargs in circuit.data:
        if instr.name == "cz":
            q_idxs = [circuit.qubits.index(q) for q in qargs]
            if tuple(sorted(q_idxs)) in cz_pairs:
                continue  # skip this CZ
        # Map qargs and cargs to new circuit's qubits/bits
        mapped_qargs = [qubit_map[q] for q in qargs]
        new_circ.append(instr, mapped_qargs, cargs)
    return new_circ


qc_trimmed = remove_selected_czs(qc, set(czs_to_cut))

# Step 4: Define qubit groups based on partition
group0 = [0, 1, 3, 4, 5, 8, 10, 12, 15, 19, 21, 24, 28, 29, 30, 34, 37, 39, 40, 41, 42, 43]
group1 = [2, 6, 7, 9, 11, 13, 14, 16, 17, 18, 20, 22, 23, 25, 26, 27, 31, 32, 33, 35, 36, 38]

# Step 5: Extract fragments by filtering operations to specific qubits
def extract_fragment(circuit, qubit_subset):
    qc_frag = QuantumCircuit(len(qubit_subset))
    qubit_map = {q: i for i, q in enumerate(qubit_subset)}
    for instr, qargs, cargs in circuit.data:
        q_idxs = [circuit.qubits.index(q) for q in qargs]
        if all(q in qubit_subset for q in q_idxs):
            new_qargs = [qc_frag.qubits[qubit_map[q]] for q in q_idxs]
            qc_frag.append(instr, new_qargs, cargs)
    return qc_frag

frag0 = extract_fragment(qc_trimmed, group0)
frag1 = extract_fragment(qc_trimmed, group1)

# Step 6: Run on BlueQubit's MPS backend
bq = bluequbit.init("h5Mo2Gt2ZUqQNmcWouBOcvPw7FlO5MzS")

result0 = bq.run(frag0, device='cpu', shots=10000)
result1 = bq.run(frag1, device='cpu', shots=10000)

counts0 = result0.get_counts()

counts1 = result1.get_counts()

# Step 7: Combine most probable results manually
peak0 = max(counts0, key=counts0.get)
peak1 = max(counts1, key=counts1.get)

print(counts0[peak0])
print(counts1[peak1])
# The fragments each return a bitstring in reverse order; fix if needed:
peak0 = peak0[::-1]
peak1 = peak1[::-1]


# Step 8: Reconstruct full bitstring by aligning group0 and group1
full_bitstring = ['0'] * qc.num_qubits
for i, q in enumerate(group0):
    full_bitstring[q] = peak0[i]
for i, q in enumerate(group1):
    full_bitstring[q] = peak1[i]

# Final peaked bitstring:
print("🎯 Most probable reconstructed bitstring:")
print("".join(full_bitstring))
