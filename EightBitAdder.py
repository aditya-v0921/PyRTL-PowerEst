import pyrtl

def build_adder():
    A = pyrtl.Input(8, 'A')
    B = pyrtl.Input(8, 'B')

    SUM = pyrtl.Output(8, 'SUM')
    CARRY = pyrtl.Output(1, 'CARRY')

    result = A + B
    SUM <<= result[0:8]
    CARRY <<= result[8]