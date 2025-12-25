import trace

import pyrtl

A = pyrtl.Input(8, 'A')
B = pyrtl.Input(8, 'B')

SUM = pyrtl.Output(8, 'SUM')
CARRY = pyrtl.Output(1, 'CARRY')
#fullSum = pyrtl.Output(9, "fullSum")

result = A + B
SUM <<= result[0:8]
CARRY <<= result[8]

sim_trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer=sim_trace)

dict_ab = {'A' : [0b00000000, 0b10010101, 0b10101010, 0b10100010], 'B' : [0b00000000, 0b10010111, 0b11110101, 0b10000100]}
dict_values = {'A' : [int(dict_ab['A'][0]), int(dict_ab['A'][1]), int(dict_ab['A'][2]), int(dict_ab['A'][3])],
               'B' : [int(dict_ab['B'][0]), int(dict_ab['B'][1]), int(dict_ab['B'][2]), int(dict_ab['B'][3])]}
sim.step_multiple(dict_ab)

def count_toggles(trace, wire_name):
    values = trace.trace[wire_name]
    togglesPerBit = [0] * 8
    for i in range(len(values)-1):
        print(f"Binary: {bin(values[i])}, Decimal: {values[i]}")
        prevVal = values[i]
        newVal = values[i+1]
        for j in range(8):
            if (prevVal << j) & 1 != (newVal << j) & 1:
                togglesPerBit[j] += 1
    return togglesPerBit

# sum_toggles = count_toggles(sim_trace, 'SUM')
# carry_toggles = count_toggles(sim_trace, 'CARRY')
# num_cycles = len(dict_ab['A'])
# toggle_rate = (sum_toggles / num_cycles)
#
# sim_trace.render_trace()

#print(f"A/B Values: {dict_values}")
print(f"8-bit Sum: {sim_trace.trace['SUM']}")
print(f"8-bit Carry: {sim_trace.trace['CARRY']}")
#print(f"SUM toggles: {sum_toggles}")
#print(f"Carry toggles: {carry_toggles}")
#print(f"Alpha (Toggle Rate) Value: {toggle_rate}")

print(count_toggles(sim_trace, 'SUM'))