import bluequbit
import qiskit

# Define a simple quantum circuit using Qiskit
from qiskit import QuantumCircuit, transpile

qc = QuantumCircuit.from_qasm_file('P2_swift_rise.qasm')

qc.draw('mpl')
# bq = bluequbit.init("tbtC35WEFeL9IXYkJoeUgFIoQzYu8lQQ")
# result = bq.run(qc, device='cpu') 
# print(result.get_statevector())