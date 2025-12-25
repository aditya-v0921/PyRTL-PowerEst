import pyrtl

def one_bit_add (a,b, carry_in):
    assert len(a) == len(b) == 1
    sum = a^b^carry_in #operators on WireVectors build the hardware
    carry_out = a & b | a & carry_in | b & carry_in
    return sum, carry_out

def ripple_add (a,b, carry_in = 0):
    a, b= pyrtl.match_bitwidth(a,b)
    if len(a) == 1:
        submits, carry_out = one_bit_add(a, b, carry_in)
    else:
        lsbit, ripplecarry = one_bit_add(a[0], b[0], carry_in)
        msbits, carry_out = ripple_add(a[1:], b[1:], ripplecarry)
        submits = pyrtl.concat(msbits, lsbit)
    return submits, carry_out

# instantiate an adder into a 3-bit counter
counter = pyrtl.Register(bitwidth = 2, name= 'counter')
sum, carry_out = ripple_add(counter, pyrtl.Const("1'b1"))
counter.next <<= sum

# simulate the instantiated design for 15 cycles
sim_trace = pyrtl.SimulationTrace()
sim = pyrtl.Simulation(tracer = sim_trace)
for cycle in range (15):
    sim.step({})
sim_trace.render_trace()