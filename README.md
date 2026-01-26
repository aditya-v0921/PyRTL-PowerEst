# PyRTL-PowerEst
Power Estimator for Circuits in Python RTL (Register-Transfer-Level) Library

Arguments (args):
    inputGenerator: Function returning a generator that yields input dicts per cycle.
        - Dict keys must match your pyrtl.Input wire names.
    capacitanceF: Capacitance per bit in Farads (default: 1)
    voltage: Supply voltage in Volts (default: 1.0V)
    clockFreqHz: Clock frequency in Hz (default: 50MHz)
    block: pyrtl.Block to simulate. If NONE, uses pyrtl.working_block()
