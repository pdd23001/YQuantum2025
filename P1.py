import bluequbit
import qiskit

# Define a simple quantum circuit using Qiskit
from qiskit import QuantumCircuit, transpile

qc = QuantumCircuit.from_qasm_file('P1_little_peak.qasm')

bq = bluequbit.init("tbtC35WEFeL9IXYkJoeUgFIoQzYu8lQQ")
result = bq.run(qc, device='cpu') 
